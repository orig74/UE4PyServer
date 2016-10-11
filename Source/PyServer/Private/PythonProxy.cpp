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

PyObject *initModule=NULL;
void* phandle=NULL;

void InitPythonFunctions()
{
	phandle=dlopen(PYTHON_LIB,RTLD_LAZY);
	_Py_Initialize=reinterpret_cast<void (*)()>(dlsym(phandle,"Py_Initialize"));
	PyRun_SimpleString=reinterpret_cast<void (*)(const char*)>(dlsym(phandle,"PyRun_SimpleString"));
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
	}

}


void StopPythonInterperter()
{
	//TODO:
	//TODO: call PyFinalize
	UE_LOG(LogTemp, Warning, TEXT("StopPythonInterperter...\n")); 
}
//TFunction<void> SampleTimerExpired();

void mytick()
{
	PYRUN("PyTick()");
}

void mybeginplay()
{
	PYRUN("from pyinit import *");
	char tmpstr[1024];
	sprintf(tmpstr,"PyBeginPlay('%p')",reinterpret_cast<void*>(GWorld->GetWorld()));
	PYRUN(tmpstr);	
}

void myendplay()
{
	char tmpstr[1024];
	sprintf(tmpstr,"PyEndPlay('%p')",reinterpret_cast<void*>(GWorld->GetWorld()));
	PYRUN(tmpstr);	
	
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
	char tmpstr[1024];
	sprintf(tmpstr,"PyInit('%p')",reinterpret_cast<void*>(GWorld->GetWorld()));
	PYRUN(tmpstr);	

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
