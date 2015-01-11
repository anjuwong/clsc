<!DOCTYPE html>
<html>
<head>
<title>
Enrollment History
</title>
</head>
<body>
<h1>Enrollment History</h1>
<p>View course enrollment as seen throughout the quarters.</p>

<?php
$db_hst = "localhost";
$db_nam = "registrar";

$sql_info = fopen("/Users/andrew/mysqlinfo","r");
$db_usr = fgets($sql_info);
$db_pss = fgets($sql_info);
fclose($sql_info);
$db_usr = str_replace("\0","",$db_usr);
$db_pss = str_replace("\0","",$db_pss);
$db_usr = str_replace("\n","",$db_usr);
$db_pss = str_replace("\n","",$db_pss);
$db_con = mysqli_connect($db_hst,$db_usr,$db_pss);
$db = mysqli_select_db($db_con,$db_nam);

/* Form for picking term + dept */
printf("<form action='index.php' method='get'>");

/* Display list of terms */
$termquery = "SELECT DISTINCT term FROM Course ORDER BY term";
$termlist = mysqli_query($db_con,$termquery);
printf("<select name='term'>\n");
while($term = mysqli_fetch_row($termlist))
    printf("    <option value='$term[0]'>$term[0]</option>\n");
printf("</select>\n");

/* Display list of depts */
$deptquery = "SELECT DISTINCT dept FROM Course ORDER BY dept";
$deptlist = mysqli_query($db_con,$deptquery);
printf("<select name='dept'>\n");
while($dept = mysqli_fetch_row($deptlist))
    printf("    <option value='$dept[0]'>$dept[0]</option>\n");
printf("</select>\n<br>");
printf('<input type ="submit" value="Get Classes">');
printf("</form>\n");

/* If both are set, then get the offered classes */
if (isset($_GET["term"]) && isset($_GET["dept"]))
{
    $t = $_GET["term"];
    $d = $_GET["dept"];
    /*printf("<script type='text/javascript'>\n");
    printf("document.getElementById('term').value='$t'\n");
    printf("document.getElementById('dept').value='$d'\n");
    printf("</script>\n");*/
    $classlist = mysqli_query($db_con,"SELECT class FROM Course WHERE term='$t' AND dept='$d' ORDER BY class");
    printf("<form action='index.php' method='get'>");
    printf("<select name='class'>\n");
    while($class = mysqli_fetch_row($classlist))
        printf("    <option value='$class[0]'>$class[0]</option>\n");
    printf("</select>\n<br>");
    printf("<input type='hidden' name='term' value='$t'>");
    printf("<input type='hidden' name='dept' value='$d'>");
    printf('<input type="submit" value="See history">');
    printf("</form>");
    if (isset($_GET["class"]))
    {
        $c = $_GET["class"];
        $enrquery = "SELECT enrollcount,timestamp FROM Enroll, Course, Lect WHERE Enroll.lectid = Lect.lectid AND Course.courseid = Lect.courseid AND term = '$t' AND dept = '$d' AND class = '$c' ORDER BY timestamp";
        printf("<h2>$t $d $c</h2>\n");
        printf("$enrquery<br>\n");
        $enrlist = mysqli_query($db_con,$enrquery);
        while($enr = mysqli_fetch_row($enrlist))
            printf("$enr[0] on $enr[1]<br>");
    }
}

/*
SELECT enrollcount
FROM Enroll e,Course c,Lect l
WHERE e.lectid = c.lectid AND c.courseid = l.courseid
    AND term = "14W" AND dept = "COM SCI" AND class = "31"
GROUP BY lectid
*/
?>
</body>
</html>
