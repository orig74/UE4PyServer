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


void (*_Py_Initialize)();
void (*PyRun_SimpleString)(const char*);
PyObject * (*_PyImport_ImportModule)(const char*);
PyObject * (*_PyObject_GetAttrString)(PyObject*,const char*);
int (*_PyCallable_Check)(PyObject*);
PyObject * (*_PyObject_CallObject)(PyObject*,PyObject*);
PyObject * (*_PyLong_FromLong)(long);
PyObject * (*_PyTuple_New)(Py_ssize_t);
int (*_PyTuple_SetItem)(PyObject *, Py_ssize_t , PyObject *);

PyObject *initModule=NULL;
void* phandle=NULL;

void InitPythonFunctions()
{
	phandle=dlopen(PYTHON_LIB,RTLD_LAZY);
	_Py_Initialize=reinterpret_cast<void (*)()>(dlsym(phandle,"Py_Initialize"));
	PyRun_SimpleString=reinterpret_cast<void (*)(const char*)>(dlsym(phandle,"PyRun_SimpleString"));
	_PyImport_ImportModule=reinterpret_cast<PyObject* (*)(const char*)>(dlsym(phandle,"PyImport_ImportModule"));
	_PyObject_GetAttrString=reinterpret_cast<PyObject* (*)(PyObject*,const char*)>(dlsym(phandle,"PyObject_GetAttrString"));
	_PyCallable_Check=reinterpret_cast<int (*)(PyObject*)>(dlsym(phandle,"PyCallable_Check"));
	_PyObject_CallObject=reinterpret_cast<PyObject* (*)(PyObject*,PyObject*)>(dlsym(phandle,"PyObject_CallObject"));
	_PyLong_FromLong=reinterpret_cast<PyObject* (*)(long)>(dlsym(phandle,"PyLong_FromLong"));
	_PyTuple_New=reinterpret_cast<PyObject* (*)(Py_ssize_t)>(dlsym(phandle,"PyTuple_New"));
	_PyTuple_SetItem=reinterpret_cast<int (*)(PyObject *, Py_ssize_t , PyObject *)>(dlsym(phandle,"PyTuple_SetItem"));
}


void LoadPythonInterperter()
{

	if (phandle==NULL)
	{
		UE_LOG(LogTemp, Warning, TEXT("Starting LoadPythonInterperter...\n"));
		//printf("---%d %d %s\n",phandle,Py_Initialize,PYTHON_LIB);
		InitPythonFunctions();
		(*_Py_Initialize)();
		PYRUN("import sys;sys.path.append('" SYSPATH "')");
		PYRUN("from pyinit import *");
		initModule = (*_PyImport_ImportModule)("pyinit");
		if (initModule != NULL) {
			PyObject *pFunc = (*_PyObject_GetAttrString)(initModule, "PyInit");
			if (pFunc && (*_PyCallable_Check)(pFunc)) {
				PyObject *aArgs=(*_PyTuple_New)(1);
				PyObject *pValue=(*_PyLong_FromLong)(500L);
				(*PyTuple_SetItem)(aArgs,0,pValue);		
				(*_PyObject_CallObject)(pFunc,aArgs);
				Py_XDECREF(pValue);
				Py_XDECREF(aArgs);
			} else {
				UE_LOG(LogTemp, Warning, TEXT("cant find function PyTick\n")); 
			}	
			Py_XDECREF(pFunc);
		} else {
			UE_LOG(LogTemp, Warning, TEXT("cant find module pyinit\n")); 
		}
	
	}

}


void StopPythonInterperter()
{
	//TODO:
	Py_XDECREF(initModule);
	//TODO: call PyFinalize
	UE_LOG(LogTemp, Warning, TEXT("StopPythonInterperter...\n")); 
}
//TFunction<void> SampleTimerExpired();

void mytick()
{
	PYRUN("mytick()");
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
