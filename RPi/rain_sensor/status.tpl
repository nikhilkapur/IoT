<!DOCTYPE html>
<html>
  <head>
    <title>Rain Sensor Status</title>
  </head>
  <body>
    <h2> Rain Sensor Status </h2>
    <hr>
    State (On/Off/Error):
      {{data["status"]["state"]}} 
    <p>
    Error: {{data["status"]["error"]}}

    <p>
    Last Check: {{data["status"]["last_check"]}}

    <p>
    Details:
		<table border=1>
		<tr> 
			<th>Day</th> 
			<th>Actual Rain</th> 
			<th>Threshold</th> 
			<th>State</th>
		</tr>
		% for day in sorted(data["daily_stats"].keys()):
		 % d = "%d-%02d-%02d" % (day.year, day.month, day.day)
		   <tr>
		   	<td>{{d}} </td> 
		   	<td>{{data['daily_stats'][day]['precip']}}</td>
		   	<td>{{data['daily_stats'][day]['precip_threshold']}}</td>
		   	<td>{{data['daily_stats'][day]['state']}}</td>
		   </tr>
		% end
		</table>
    <p>
	 Config
	  <!-- <form method="get" action="/update"> -->
	  <form method="get" action="rs_server.py">
      	<label>ZIP<input name="zipcode" type="text" value="{{data['config']['zipcode']}}"> </label>
        <input name=command type=hidden value=update>
      	<p>
      	<input type="submit" value="Update">
      </form>
  </body>
</html>

