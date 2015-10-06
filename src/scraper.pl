#!/usr/bin/perl -w

print "\n";

#get current teaching period
%semest1 = (
        Jan => "1",
        Feb => "2",
        Mar => "3",
        Apr => "4",
        May => "5",
        Jun => "6",
        Dec => "12",
);
$currMonth = `date +%b`;
$currYear = `date +%G`;
chomp $currYear;

#$currMonth = "Jan"; #pretend we are semester 1
if (exists($semest1{$currMonth})) {
        $currentSem = 1;
} else {
        $currentSem = 2;
}

#loop over each course
foreach $subject (<STDIN>) {
        chomp $subject;
        print "    //              $subject              //\n";
        print "    //             Semester $currentSem             //\n";
        #print "+----------------------+\n";
        $url = "http://www.timetable.unsw.edu.au/$currYear/$subject.html";
        #open SITE, "wget -q -O- $url" or die; # for some reason this doesnt work for me
        $content = `wget -q -O- "$url"` or die "$!";
        @content = split(/\n/m, $content);

        #flags and counters
        $i = 20;
        $lineNum = 0;
        $detailFlag = 0;
        $notesFlag = 1;
        $nextLineCapture = 0;
        $captureCapacity = 0;
        $weeksFlag = 0;

        foreach $line (@content) {
                chomp $line;
                #
                #CHECK THE CAPACITY OF THE CLASS
                #
                if ($captureCapacity == 1) {
                }

                #flag for whether or not the details section has been reached
                if ($line =~ '\- Detail') {
                        $detailFlag = 1;
                }

                # detect the current activity
                if ($nextLineCapture == 1) {
                        $currLine = $line;
                        #$currLine =~ s/\<.+?\>([A-Za-z]+)/$1/g;
                        $currLine =~ s/\<.+?\>//g;
                        $currLine =~ s/^\ +//g;
                        $currLine =~ s/\ $//g;
                        print "    $currLine\n";
                        $nextLineCapture = 0;
                }
                if ($line =~ 'label\"\>Activity') {
                        $nextLineCapture = 1;
                }

                # account for whether or not you need more than 1 tutorial
                # that is not in the same stream e.g calc/algebra for
                # MATH1131, MATH1141, etc
                if ($line =~ 'Tutorial ([0-9]) of ([0-9])' && $detailFlag == 1) {
                        $tutCurr = $1;
                        $tutNeed = $2;
                        #print "Select $tutNeed tutorial(s)\n";
                        print "    $tutCurr of $tutNeed\n";
                }

                if ($line =~ 'Class Notes') {
                        print "------------------------\n";
                        $notesFlag = 1;
                }

                #sanitise the current line
                $line =~ s/^\ +//g;                             #remove space
                $line =~ s/\<(.+?)\>//g;                        #remove tags

                #skip newly blanked lines
                if ($line =~ '^\ *$') {
                        $i++;
                        $lineNum++;
                        next;
                }

                if ($line =~ '[0-9]+\-[0-9]\,') {
                        $weeksFlag = 1;
                        $i++;
                        $lineNum++;
                        next;
                }

                if ($line =~ 'Instructor' && $detailFlag == 1) {
                        #print "$lineNum\:$line \n";
                        #print "\n";
                        $i = 0;
                        $notesFlag = 0;
                        next;
                }
                if($notesFlag == 0 && $detailFlag == 1) {
                        print "    $line \n";
                        $lineNum++;
                        next;
                }

                $i++;
                $lineNum++;

        }
        #close(SITE);
}