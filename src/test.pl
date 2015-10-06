#!/usr/bin/env perl -w

$url = "http://www.timetable.unsw.edu.au/2015/COMP2041.html";
#print "$url";
$content = `wget -q -O- "$url"` or die;
@content = $content =~ /\n/g;
print scalar @content;