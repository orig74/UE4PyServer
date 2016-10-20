# UE4PyServer
<h3>Unreal Engine Python Plugin</h3>

<h4>Installation:<br/>
1. create a project in unreal engine<br/>
2. an empty c++ class so the project will be a code project<br/>
3. close the project<br/>
4. in project dir create Plugin dir<br/>
5. clone Pyserver to that dir<br/>
6. cd to:<br/>
[ProjectPath]/Plugins/PyServer/Source/PyServer<br/>
7. run: <br/>
python config.py --entry_point track_test<br/>
8. run:<br/>
python build.py --engine-path=<<unreal engine dir PATH>><br/>


9. for running in stand alone game add -nocore to the additional launch parameters in the advanced settings of the play button<br/>
10. Add Camera CameraActor_2<br/>
11. Add wind WindDirectionalSource1<br/>
