# UE4PyServer
Unreal Engine Python Plugin
to install plugin:
1. create a project in unreal engine
2. an empty c++ class so the project will be a code project
3. close the project
4. in project dir create Plugin dir
5. clone Pyserver to that dir
6. cd to:
[ProjectPath]/Plugins/PyServer/Source/PyServer
7. run: 
python config.py --entry_point track_test
8. run:
python build.py --engine-path=<<unreal engine dir PATH>>


9. for running in stand alone game add -nocore to the additional lanch parameters in the addvanced settings of the play button
10. Add Camera CameraActor_2
11. Add wind WindDirectionalSource1
