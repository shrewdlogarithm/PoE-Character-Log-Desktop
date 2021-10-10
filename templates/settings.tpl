% import utils
<link rel="stylesheet" href="/css/style.css">
<link rel="stylesheet" href="/css/poe.css">
% setdefault('message', '')
<font size=22>{{message}}</font>
<form method="post" action="savesettings" enctype="multipart/form-data">
    <table>
        <tr><td>Client.txt path </td><td><input name="clientlog" value="{{utils.getopt("clientlog")}}" type="text"></td></tr>
        <tr><td>Account Name</td><td><input name="account" value="{{utils.getopt("account")}}" type="text"></td></tr>
    </table>
    <input type="submit">    
</form>
<p><a href="{{utils.homep}}">Version: {{utils.vers}}</a></p>
