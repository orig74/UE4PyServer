// Copyright 1998-2016 Epic Games, Inc. All Rights Reserved.
#include "PyServerPrivatePCH.h"

#include "SlateBasics.h"
#include "SlateExtras.h"

#include "PyServerStyle.h"
#include "PyServerCommands.h"

#include "LevelEditor.h"

#include "PythonProxy.h"

static const FName PyServerTabName("PyServer");

#define LOCTEXT_NAMESPACE "FPyServerModule"

void FPyServerModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
	
	FPyServerStyle::Initialize();
	FPyServerStyle::ReloadTextures();
	LoadPythonInterperter();
	FPyServerCommands::Register();
	
	PluginCommands = MakeShareable(new FUICommandList);

	PluginCommands->MapAction(
		FPyServerCommands::Get().PluginAction,
		FExecuteAction::CreateRaw(this, &FPyServerModule::PluginButtonClicked),
		FCanExecuteAction());
		
	FLevelEditorModule& LevelEditorModule = FModuleManager::LoadModuleChecked<FLevelEditorModule>("LevelEditor");
	
	{
		TSharedPtr<FExtender> MenuExtender = MakeShareable(new FExtender());
		MenuExtender->AddMenuExtension("WindowLayout", EExtensionHook::After, PluginCommands, FMenuExtensionDelegate::CreateRaw(this, &FPyServerModule::AddMenuExtension));

		LevelEditorModule.GetMenuExtensibilityManager()->AddExtender(MenuExtender);
	}
	
	{
		TSharedPtr<FExtender> ToolbarExtender = MakeShareable(new FExtender);
		ToolbarExtender->AddToolBarExtension("Settings", EExtensionHook::After, PluginCommands, FToolBarExtensionDelegate::CreateRaw(this, &FPyServerModule::AddToolbarExtension));
		
		LevelEditorModule.GetToolBarExtensibilityManager()->AddExtender(ToolbarExtender);
	}
}

void FPyServerModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
	FPyServerStyle::Shutdown();

	FPyServerCommands::Unregister();
}

void FPyServerModule::PluginButtonClicked()
{
	// Put your "OnButtonClicked" stuff here
	/*
	   FText DialogText = FText::Format(
	   LOCTEXT("PluginButtonDialogText", "Add code to {0} in {1} to override this button's actions!!!"),
	   FText::FromString(TEXT("FPyServerModule::PluginButtonClicked()")),
	   FText::FromString(TEXT("PyServer.cpp"))
	   );
	FMessageDialog::Open(EAppMsgType::Ok, DialogText);
	 */

	PythonButtonClicked();
}

void FPyServerModule::AddMenuExtension(FMenuBuilder& Builder)
{
	Builder.AddMenuEntry(FPyServerCommands::Get().PluginAction);
}

void FPyServerModule::AddToolbarExtension(FToolBarBuilder& Builder)
{
	Builder.AddToolBarButton(FPyServerCommands::Get().PluginAction);
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FPyServerModule, PyServer)
