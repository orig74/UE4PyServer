# UE4PyServer
<h2>Unreal Engine Python Plugin</h2>

<h3>Installation: (For now Linux Only)</h3><br/>
<h4>Prerequisits</h4>
- Unreal Engine for linux installation:  <a href="https://wiki.unrealengine.com/Building_On_Linux">UE4</a><br/>
- Python 3.x installation<br/>
<h4>Prerequisits For Otical-Flow Demo</h4>
- OpenCv for Python 3<br/>
- numpy<br/>
<h4>Plugin Setup</h4>
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
