# UE4PyServer
<h3>Unreal Engine Python Plugin</h3>

<h4>Installation: (For now Linux Only)</h4><br/>
- Create a project in unreal engine:<br/>
- Add an empty c++ class so the project will be a code project<br/>
- Close the project<br/>
- In the project dir create Plugin dir<br/>
- Clone UE4PyServer to that dir<br/>
git clone  https://github.com/origanoni/UE4PyServer.git<br/>
- cd to:  [ProjectPath]/Plugins/UE4PyServer/Source/PyServer<br/>
- run: <br/>
python config.py --entry_point <your entry point><br/>
for the test demo run:<br/>
python config.py --entry_point track_test
- run:<br/>
python build.py --engine-path=<<unreal engine dir PATH>><br/>

<h4>Running The Demo:</h4>
The demo is "Lucas-Kanade optical flow tracking" from OpenCV library.  For the purpose of the demo I installed python 3.5 Anaconda <a href="https://www.continuum.io/downloads" >Anaconda</a>. <br/>
Add Camera CameraActor_2<br/>
11. Add wind WindDirectionalSource1<br/>
