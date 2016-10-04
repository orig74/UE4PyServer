#ifndef TESTING_ONLY
#include "PyServerPrivatePCH.h"
#include "UnrealClient.h"
#include "ImageUtils.h"
#include "TimerManager.h"
#include "PyServerTickActor.h"
#else
#define LogTemp 0
#define Warning 0
#define TEXT(x) x
#define UE_LOG(arg1,arg2,...)  printf(__VA_ARGS__)

#endif


#include <dlfcn.h>



//#include  "/local/ori/anaconda3/include/python3.5m/Python.h"
extern "C" {
//#define PYTHON_LIB "/local/ori/anaconda3/lib/libpython3.5m.so"
//#define SYSPATH "local/learn/ur4/testplugin/Plugins/PyServer/Source/PyServer/Private"

//#include PYTHON_H
#include "PyConfig.h"



#define PYRUN(x) (*PyRun_SimpleString)(x)
//#error stopping!

void* phandle=NULL;

void (*PyRun_SimpleString)(const char*);
PyObject * (*_PyImport_ImportModule)(const char*);
PyObject * (*_PyObject_GetAttrString)(PyObject*,const char*);
int (*_PyCallable_Check)(PyObject*);
PyObject * (*_PyObject_CallObject)(PyObject*,PyObject*);

void InitPythonFunctions()
{
	PyRun_SimpleString=reinterpret_cast<void (*)(const char*)>(dlsym(phandle,"PyRun_SimpleString"));
	_PyImport_ImportModule=reinterpret_cast<PyObject* (*)(const char*)>(dlsym(phandle,"PyImport_ImportModule"));
	_PyObject_GetAttrString=reinterpret_cast<PyObject* (*)(PyObject*,const char*)>(dlsym(phandle,"PyObject_GetAttrString"));
	_PyCallable_Check=reinterpret_cast<int (*)(PyObject*)>(dlsym(phandle,"PyCallable_Check"));
	_PyObject_CallObject=reinterpret_cast<PyObject* (*)(PyObject*,PyObject*)>(dlsym(phandle,"PyObject_CallObject"));
}


void LoadPythonInterperter()
{

	if (phandle==NULL)
	{
		phandle=dlopen(PYTHON_LIB,RTLD_LAZY);
		void (*Py_Initialize)();
		UE_LOG(LogTemp, Warning, TEXT("Starting LoadPythonInterperter...\n"));
		Py_Initialize=reinterpret_cast<void (*)()>(dlsym(phandle,"Py_Initialize"));
		//printf("---%d %d %s\n",phandle,Py_Initialize,PYTHON_LIB);
		InitPythonFunctions();
		(*Py_Initialize)();
		PYRUN("import sys;sys.path.append('" SYSPATH "')");
		PYRUN("from pyinit import *");
		
	}

}

//TFunction<void> SampleTimerExpired();

void mytick()
{
	PyObject *pModule=NULL, *pDict=NULL, *pFunc=NULL;
	//pName = PyUnicode_DecodeFSDefault("pyinit.py");
	//pModule = PyImport_Import(pName);
	//Py_DECREF(pName);
	pModule = (*_PyImport_ImportModule)("pyinit");
	
	if (pModule != NULL) {
		pFunc = (*_PyObject_GetAttrString)(pModule, "PyTick");
		if (pFunc && (*_PyCallable_Check)(pFunc)) {
			(*_PyObject_CallObject)(pFunc,NULL);
		} else {
			UE_LOG(LogTemp, Warning, TEXT("cant find function PyTick\n")); 
		}	
	} else {
		UE_LOG(LogTemp, Warning, TEXT("cant find module pyinit\n")); 
	}
	Py_XDECREF(pFunc);
	
	Py_XDECREF(pModule);
}


int calledfrompython()
{
	printf("yo!!!\n");
	UE_LOG(LogTemp, Warning, TEXT("Called from python\n")); 
	FString filename = "/tmp/test1.png";
	FScreenshotRequest::RequestScreenshot(filename, false, false);
	return 0;
}


void PythonButtonClicked()
{
	PYRUN("import pyinit;import imp;imp.reload(pyinit)");
	PYRUN("PythonButtonClicked()");
	//UGameViewportClient* ViewportClient = GWorld->GetGameViewport();
	//FViewport* InViewport = ViewportClient->Viewport;
	//FIntVector Size(InViewport->GetSizeXY().X, InViewport->GetSizeXY().Y, 0);
	{
		FString filename = "/tmp/test.png";
		FScreenshotRequest::RequestScreenshot(filename, false, false);
	}

	//myActor1=NewObject<APyServerTickActor>();

	bool isSpawned=false;

	for (TActorIterator<APyServerTickActor> ActorItr(GWorld); ActorItr; ++ActorItr)
	{
		UE_LOG(LogTemp, Warning, TEXT("already having APyServerTickActor not spawinning\n"));
		isSpawned=true; 
	}	
	if (!isSpawned)
	{
		FActorSpawnParameters SpawnInfo;
		GWorld->SpawnActor<APyServerTickActor>(APyServerTickActor::StaticClass(), FVector(0.0f), FRotator(0, 0, 0), SpawnInfo);
		isSpawned=true;
	}
	//FTicker::GetCoreTicker().AddTicker(FTickerDelegate::CreateRaw(&mytick), 1.0f);
	//GWorld->GetTimerManager().SetTimer(SampleTimerHandle, &SampleTimerExpired, 1.0f, false,1.0f);
	//GWorld->GetTimerManager().SetTimerForNextTick(&SampleTimerExpired);
	//FString CaptureFilename("/tmp/out.png");

	//TArray<FColor> Bitmap(Size);
	//bool bScreenshotSuccessful = false;
	//bScreenshotSuccessful = GetViewportScreenShot(InViewport, Bitmap);
	// InViewport->ReadFloat16Pixels

	//if (bScreenshotSuccessful)
	//{
	// Ensure that all pixels' alpha is set to 255
	//for (auto& Color : Bitmap)
	//{
	//	Color.A = 255;
	//}
	// TODO: Need to blend alpha, a bit weird from screen.

	//TArray<uint8> CompressedBitmap;
	//FImageUtils::CompressImageArray(Size.X, Size.Y, Bitmap, CompressedBitmap);
	//FFileHelper::SaveArrayToFile(CompressedBitmap, *CaptureFilename);
	//}else
	//{
	//	UE_LOG(LogTemp, Warning, TEXT("Faild capture screen!!"));	
	//}


	
}



}//extern "C"
