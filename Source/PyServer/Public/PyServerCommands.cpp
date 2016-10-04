// Copyright 1998-2016 Epic Games, Inc. All Rights Reserved.

#include "PyServerPrivatePCH.h"
#include "PyServerCommands.h"

#define LOCTEXT_NAMESPACE "FPyServerModule"

void FPyServerCommands::RegisterCommands()
{
	UI_COMMAND(PluginAction, "PyServer", "Execute PyServer action", EUserInterfaceActionType::Button, FInputGesture());
}

#undef LOCTEXT_NAMESPACE
