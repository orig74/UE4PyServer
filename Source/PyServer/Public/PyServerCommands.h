// Copyright 1998-2016 Epic Games, Inc. All Rights Reserved.

#pragma once

#include "SlateBasics.h"
#include "PyServerStyle.h"

class FPyServerCommands : public TCommands<FPyServerCommands>
{
public:

	FPyServerCommands()
		: TCommands<FPyServerCommands>(TEXT("PyServer"), NSLOCTEXT("Contexts", "PyServer", "PyServer Plugin"), NAME_None, FPyServerStyle::GetStyleSetName())
	{
	}

	// TCommands<> interface
	virtual void RegisterCommands() override;

public:
	TSharedPtr< FUICommandInfo > PluginAction;
};
