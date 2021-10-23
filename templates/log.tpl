<link rel="stylesheet" href="/css/style.css">
<link rel="stylesheet" href="/css/poe.css">
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
    lastlog = ""
    function logreader() {
        $.ajax({
            type: "POST",
            url: '/logdata', 
            data: {"lastlog": lastlog},
            success: function(data) {
                $.each(data["loglines"],function(ln,li) {
                    $("#log").prepend("<tr><td>" + li + "</td></tr>")
                    lastlog = li.substring(0,20)
                })                    
            },
            complete: function() {
                setTimeout(logreader, 5000);
            }
      })
    }
    $(document).ready(function(){
        logreader()
    });
</script>
<table id="log">
</table>