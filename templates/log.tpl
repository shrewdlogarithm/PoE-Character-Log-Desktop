% import utils
<link rel="stylesheet" href="/css/style.css">
<link rel="stylesheet" href="/css/poe.css">
<table>
%with open("poeclog.log") as logfile:
%  lines = logfile.readlines()
%  for line in lines:
    <tr><td>{{line}}</td></tr>
%  end
%end
</table>