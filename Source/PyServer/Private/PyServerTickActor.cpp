// Fill out your copyright notice in the Description page of Project Settings.

#include "PyServerPrivatePCH.h"
#include "Engine.h"
#include "PyServerTickActor.h"
#include "PythonProxy.h"


// Sets default values
APyServerTickActor::APyServerTickActor()
{
 	// Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
	PrimaryActorTick.bCanEverTick = true;
	UE_LOG(LogTemp, Warning, TEXT("Init APyServerTickActor\n"));
}

// Called when the game starts or when spawned
void APyServerTickActor::BeginPlay()
{
	Super::BeginPlay();
	UE_LOG(LogTemp, Warning, TEXT("called APyServerTickActor::BeginPlay\n"));
	
}

// Called every frame
void APyServerTickActor::Tick( float DeltaTime )
{
	Super::Tick( DeltaTime );
	mytick();	

}

