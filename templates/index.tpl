% import utils
<link rel="stylesheet" href="/css/style.css">
<link rel="stylesheet" href="/css/poe.css"><table>
% for log in logs:
    <tr><td>{{log}}</td></tr>
% end
</table>
<p><a href="{{utils.homep}}">Version: {{utils.vers}}</a></p>
