#!/usr/local/bin/perl

#use strict;
use DB_File;
use CGI qw(:standard);

my $savedb = "/home/monkey/data/trek-save.db";
my $codestring = "0aceACEBDFbdf1GgHhiIKlJjLk2ZzyYXx3WvutSwVUT4Rr5NnoO6Pp7m8M9";
my $state = param(state);
my $command = param(command);



print <<HEAD;
Content-type: text/html

<head><title>$title</title></head>
<body bgcolor=000000 text=00FF00 link=00AA00 vlink=00AA00 alink=00AA00 >
<center>
<a href=http://www.monkeyplay.com/games/ target=_top onmouseover="status='Back to Monkey Play Games';return true">Back
to Monkey Play Games</a> 
</center>
<hr>
HEAD



my $e0 = 3000;
my $p0 = 10;
my $s9 = 200;

my @c = ( [0,0,-1,-1,-1,0,1,1,1,0],
	  [1,1,1,0,-1,-1,-1,0,1,1]);

my @quad_name = ("","Antares","Rigel","Procyon","Vega",
		 "Canopus","Altair","Sagittarius","Pollux",
		 "Sirius","Deneb","Capella","Betelgeuse",
		 "Aldebaran","Regulus","Arcturus","Spica");
my @sect_name = ("","I","II","III","IV");
my @device_name = ("","Warp Engines","Short Range Sensors",
		   "Long Range Sensors","Phaser Control","Photon Tubes",
		   "Damage Control","Shield Control","Library Computer");


if (param(help)) {

    my $content;
    open(HELP,"trek_help.txt") || die "Can't open help file: $!";
    { local $/ = undef;
      $content = <HELP> }
    close(HELP);

    # print help

    print <<HELP;
<a onmouseover="status='return to game';return true" href="trek.cgi">Return to game</a>
<hr/><pre>
$content
</pre><hr/>
<a onmouseover="status='return to game';return true" href="trek.cgi">Return to game</a>
HELP

}
elsif ($data{save}) {

    # save game

#$user = &ucooktest;
#($gamenum,$pnum,$gangname) = &findgame($user);
#print "No entry for $user." unless ($gamenum);


}
elsif ($data{restore}) {

    # restore game

#$user = &ucooktest;
#($gamenum,$pnum,$gangname) = &findgame($user);
#print "No entry for $user." unless ($gamenum);


}
else {
    if ($state) {
	
	print "<pre>";

	# initialize

	$state = ($state eq "init")?&initstate:&decode($state);
	if ($state eq "inited") {
	    &new_quadrant;
	    &short_range_scan;
	}
	else {
	    &parse($state);
	}

	# process turn

	$give_command = 1;

	# get grammar correct

	$sX = ($b9==1)?"":"s";
	$sX0 = ($b9==1)?"is":"are";

#	print "\nSTATE1: $state\n\n";

	if ((($s + $e)<=10)&&(($e<10)||($d[7]<0))) {
	    printf("\n** Fatal Error **   ");
	    printf("You've just stranded your ship in space.\n\n");
	    printf("You have insufficient maneuvering energy,");
	    printf(" and Shield Control is presently\n");
	    printf("incapable of cross circuiting to engine room!!\n\n");
	    &end_of_time;
	}

	if ($command eq "nav") {
	    &course_control;
	}
	elsif ($command eq "srs") {
	    &short_range_scan;
	}
	elsif ($command eq "lrs") {
	    &long_range_scan;
	}
	elsif ($command eq "pha") {
	    &phaser_control;
	}
	elsif ($command eq "tor") {
	    &photon_torpedoes;
	}
	elsif ($command eq "she") {
	    &sheild_control;
	}
	elsif ($command eq "dam") {
	    &damage_control;
	}
	elsif ($command eq "com") {
	    &library_computer;
	}
	elsif ($command eq "xxx") {
	    &resign_commision;
	}
	
#	for ($i=1;$i<=3;$i++) {
#	    for ($j=1;$j<=3;$j++) {
#		print "K $i,$j: $k[$i][$j]\n";
#	    }
#	}

	$state = &esrap;

#	print "\nSTATE2: $state\n\n";

	$state=&encode($state);

	# write HTML

	if ($give_command) {
	    print "\n<form action=trek.cgi method=post>";
	    print "<input type=hidden name=state value=\"$state\">";
	    print "Order: <select name=command>";
	    print "<option value=nav>Set Course";
	    print "<option value=srs>Short Range Sensors";
	    print "<option value=lrs>Long Range Sensors";
	    print "<option value=pha>Phasers";
	    print "<option value=tor>Photon Torpedoes";
	    print "<option value=she>Shield Control";
	    print "<option value=dam>Damage Control";
	    print "<option value=com>Library Computer";
	    print "<option value=xxx>Resign Command";
	    print "</select> <input type=submit value=\"Make It So\"></form>";
	}
    }
    else {
	
    # do game intro

	# generate initial state

	$state = "init";

	print "<pre>";
	print "\n\n";
	print " *************************************\n";
	print " *                                   *\n";
	print " *                                   *\n";
	print " *      * * Super Star Trek * *      *\n";
	print " *                                   *\n";
	print " *                                   *\n";
	print " *************************************\n\n";

	print "\nDo you need instructions (<a href=trek.cgi?help=1 onmouseover=\"status='Instructions';return true\">yes</a>/<a href=trek.cgi?state=$state onmouseover=\"status='Start Game';return true\">no</a>): ";

	print "\n\n\n";
	print "                         ------*------\n";
	print "         -------------   `---  ------'\n";
	print "         `-------- --'      / /\n";
	print "                  \\\\-------  --\n";
	print "                  '-----------'\n";
	print "\n       The USS Enterprise --- NCC - 1701\n\n\n";
	print "</pre>";
    }

}

sub initstate {

    # initialize time

    $t = int(rand(20) + 21) * 100;     # current stardate 
    $t0 = $t;                          # initial stardate
    $t9 = 26 + int(rand(10));          # end of time

    # initialize enterprise

    $d0 = 0;                # docking flag
    $e = $e0;               # energy
    $p = $p0;               # photon torpedos
    $s = 0;                 # shield power
    $q1 = int(rand(8)+1);   # quadrant x
    $q2 = int(rand(8)+1);   # quadrant y
    $s1 = int(rand(8)+1);   # sector x
    $s2 = int(rand(8)+1);   # sector y

    @d = ("0"x9);             # damage array

    # set up what exists in galaxy

    $k9 = 0;                # total klingons left

    for ($i=1;$i<=8;$i++) {
	for ($j=1;$j<=8;$j++) {
 
	    $k3 = 0;
	    $z[$i][$j] = 0;
	    $r1 = int(rand(100)+1);
	    if ($r1 > 98) {
		$k3 = 3;
	    }
	    elsif ($r1 > 95) {
		$k3 = 2;
	    }
	    elsif ($r1 > 80) {
		$k3 = 1;
	    }
	    $k9 += $k3;

	    $b3 = 0;       # starbases in quadrant
	    $b3 = 1 if (int(rand(100)+1) > 96);
	    $b9 += $b3;

	    $g[$i][$j] = $k3*100 + $b3*10 + int(rand(8)+1);

	}
    }

    $t9 = $k9 + 1 if ($k9 > $t9);

    if ($b9 == 0) {
	if ($g[$q1][$q2] < 200) {
	    $g[$q1][$q2] += 100;
	    $k9++;
	}
	$g[$q1][$q2] += 10;
	$b9++;

	$q1 = int(rand(8)+1);
	$q2 = int(rand(8)+1);
    }

    $k7 = $k9;      # klingons at start

    $sX = ($b9==1)?"":"s";
    $sX0 = ($b9==1)?"is":"are";

#    print "<pre>";
    print "Your orders are as follows:\n\n";
    print "   Destroy the $k9 Klingon warships which have invaded\n";
    print " the galaxy before they can attack Federation Headquarters\n";
    printf (" on stardate %d.  This gives you %d days.  There %s\n",
	    $t0+$t9,$t9,$sX0);
    print " $b9 starbase$sX in the galaxy for resupplying your ship.\n\n";

    $state = &esrap;
    $state = "000";
    $state = &encode($state);

#    print "<a onmouseover=\"status='Start Your Mission';return true\" href=trek.cgi?state=$state>Start Your Mission</a>";

    return "inited";

}

sub new_quadrant {
    $z4 = $q1;
    $z5 = $q2;
    $k3 = 0;     # klingons in quadrant
    $b3 = 0;     # starbases in quadrant
    $s3 = 0;     # stars in quadrant
    $g5 = 0;     # quadrant name flag
    $d4 = (int(rand(100)+1)) / 100 / 50;
    $z[$q1][$q2] = $g[$q1][$q2];

    if ($q1>=1 && $q1<=8 && $q2>=1 && $q2<=8) {
	&quadrant_name;
	if ($t0 != $t) {
	    printf("Now entering %s quadrant...\n\n",$sG2);
	}
	else {
	    print "\nYour mission begins with your starship located\n";
	    print "in the galactic quadrant $sG2.\n\n";
	}
    }

    $k3=int($g[$q1][$q2] * .01);
    $b3=int($g[$q1][$q2] * .1 - 10*$k3);
#    print "NQ - G: $g[$q1][$q2] K3: $k3 B3: $b3\n";
    $s3=$g[$q1][$q2] - 100*$k3 - 10*$b3;

    if ($k3 > 0) {
	print "Combat Area  Condition Red\n";
	print "Shields Dangerously Low\n" if ($s < 200);
    }

    for ($i=1;$i<=3;$i++) {
	$k[$i][1]=0;
	$k[$i][2]=0;
	$k[$i][3]=0;
    }

    $sQ=" "x193;

    # position enterprise, then klingons, starbases, and stars

    $sA="<*>";
    $z1=int($s1+.5);
    $z2=int($s2+.5);
    &insert_in_quadrant;

    if ($k3>0) {
	for ($i=1;$i<=$k3;$i++) {
	    $z3=0;
	    &find_empty_place;
	    $sA="+K+";
	    $z1=$r1;
	    $z2=$r2;
	    &insert_in_quadrant;
	
#	    print "R1: $r1 R2: $r2\n";

	    $k[$i][1]=$r1;
	    $k[$i][2]=$r2;
	    $k[$i][3]=100 + int(rand(200)+1);
	}
    }

    if ($b3>0) {
	&find_empty_place;
	
	$sA=">!<";
	$z1=$r1;
	$z2=$r2;
	&insert_in_quadrant;

	$b4=$r1;
	$b5=$r2;
    }

    for ($i=1;$i<=$s3;$i++) {
	&find_empty_place;
	$sA = " * ";
	$z1=$r1;
	$z2=$r2;
	&insert_in_quadrant;
    }
}

sub course_control {
    $sX = 8;
    
    if (!$data{warp}) {
	&course_control_form;
    }
    else {
	$c1 = $data{course};
	$w1 = $data{warp};
	
	$c1 = 1 if ($c1 == 9);

	if ($c1<0 || $c1>9) {
	    print "Lt. Sulu reports:\n";
	    print "  Incorrect course data, sir!\n\n";
	    return;
	}
	
	if ($d[1]<0 && $w1>.2) {
	    print "Warp Engines are damaged.\n";
	    print "Maximum speed = Warp 0.2.\n\n";
	    return;
	}

	return if ($w1<=0);

	if ($w1 > 8) {
	    print "Chief Engineer Scott reports:\n";
	    printf("  The engines won't take warp %4.1f!\n\n",$w1);
	    return;
	}

	$n=int(($w1*8)+.5);

	if ($e-$n < 0) {
	    print "Engineering reports:\n";
	    print "  Insufficient energy available for maneuvering";
	    printf( "  at warp %4.1f!\n\n",$w1);

	    if ($s >= $n && $d[7] >= 0) {
		print "Deflector Control Room acknowledges:\n";
		printf("  %d units of energy presently deployed to shields.\n",%s);
	    }

	    return;
	}

	&klingons_move;
	
	&repair_damage;

#	print "C1: $c1 W1: $w1\n";

	$sA = "   ";
	$z1 = int($s1+.5);
	$z2 = int($s2+.5);

#	print "Z1: $z1 Z2: $z2\n";

	&insert_in_quadrant;

	$c2 = int($c1+.5);
	$c3 = $c2+1;

#	print "C2: $c2 C3: $c3\n";
	
	$x1 = $c[0][$c2] + ($c[0][$c3] - $c[0][$c2]) * ($c1 - $c2);
	$x2 = $c[1][$c2] + ($c[1][$c3] - $c[1][$c2]) * ($c1 - $c2);

#	print "X1: $x1 X2: $x2\n";

	$x = $s1;
	$y = $s2;
	$q4 = $q1;
	$q5 = $q2;

	for ($i=1;$i<=$n;$i++) {
	    $s1 = $s1+$x1;
	    $s2 = $s2+$x2;
	    
	    $z1=int($s1+.5);
	    $z2=int($s2+.5);

	    if ($z1<1 || $z1>=9 || $z2 <1 || $z2>=9) {
		&exceed_quadrant_limits;
		&complete_maneuver;
		return;
	    }

	    &string_compare;
#	    print "Z1: $z1 Z2: $z2 Z3: $z3\n";
	    if ($z3 != 1) {   # sector is not empty
		$s1 = $s1-$x1;
		$s2 = $s2-$x2;
		print "Warp Engines shut down at sector ";
		printf("%d, %d due to bad navigation.\n\n",$z1,$z2);
		$i=$n+1;
	    }
	}

	&complete_maneuver;

    }
}

sub course_control_form {
    $give_command = 0;
    $state=&encode($state);

    print "<form action=trek.cgi method=post>";
    print "<input type=hidden name=command value=nav>";
    print "<input type=hidden name=state value=\"$state\">";
    print "\nCourse (0-9): <input type=text size=3 name=course><p>\n";
    $sX = "0.2" if ($d[1] < 0);
    printf ("Warp Factor (0-%s): <input type=text size=3 name=warp><p>\n",$sX);
    print "<input type=submit value=Engage></form>";
}

sub complete_maneuver {
#    print "completing maneuver...\n";

    $sA = "<*>";

    $z1=int($s1+.5);
    $z2=int($s2+.5);
    
#    print "Z1: $z1 Z2: $z2\n";

    &insert_in_quadrant;

    &maneuver_energy;

    $t8=1;

    $t8 = $w1 if ($w1<1);

    $t = $t + $t8;

    &end_of_time if ($t > $t0+$t9);

    &short_range_scan;
}

sub exceed_quadrant_limits {
    $x5 = 0;     # outside galaxy flag

#    print "S1: $s1 S2: $s2 Q1: $q1 Q2: $q2 X: $x Y: $y N: $n\n";

    $x = (8 * ($q1 - 1)) + $x + ($n * $x1);
    $y = (8 * ($q2 - 1)) + $y + ($n * $x2);

    $q1 = int($x / 8.0 + 0.9);
    $q2 = int($y / 8.0 + 0.9);
    
#    print "EQL - X: $x Y: $y N: $n X1: $x1 X2: $x2\n";
    
    $s1 = $x - (($q1 - 1) * 8);
    $s2 = $y - (($q2 - 1) * 8);
    
    if (int($s1+.5) == 0) {
	$q1 = $q1 - 1;
	$s1 = $s1 + 8;
    }
    if (int($s2+.5) == 0) {
	$q2 = $q2 - 1;
	$s2 = $s2 + 8;
    }

#    print "S1: $s1 S2: $s2 Q1: $q1 Q2: $q2 \n";

    # check if outside galaxy

    if ($q1 < 1) {
	$x5 = 1;
	$q1 = 1;
	$s1 = 1;
    }

    if ($q1 > 8) {
	$x5 = 1;
	$q1 = 8;
	$s1 = 8;
    }

    if ($q2 < 1) {
	$x5 = 1;
	$q2 = 1;
	$s2 = 1;
    }

    if ($q2 > 8) {
	$x5 = 1;
	$q2 = 8;
	$s2 = 8;
    }

    $t = $t + 1;

    if ($x5 == 1) {
	print "Lt. Uhura reports:\n";
	print "  Message from Starfleet Command:\n\n";
	print "  Permission to attempt crossing of galactic perimeter\n";
	print "  is hereby *denied*.  Shut down your engines.\n\n";
	print "Chief Engineer Scott reports:\n";
	printf("  Warp Engines shut down at sector %d, ",int($s1+.5));
	printf("%d of quadrant %d, %d.\n\n",int($s2+.5),$q1,$q2);
    }
    else {
	&new_quadrant;
    }

    &maneuver_energy;
    

    &end_of_time if ($t > $t0+$t9);
}

sub maneuver_energy {
    $e = $e - n - 10;
    
    return if ($e > 0);

    print "Shield Control supplies energy to complete maneuver.\n\n";

    $s = $s - $e;
    $e = 0;

    $s = 0 if ($s <= 0);
}

sub short_range_scan {
    $sC = "GREEN";
    $sC = "YELLOW" if ($e < $e0 * .1);
    $sC = "RED" if ($k3 > 0);
    $d0 = 0;
    for ($i=$s1-1;$i<=$s1+1;$i++) {
	for ($j=$s2-1;$j<=$s2+1;$j++) {
	    if ($i>=1 && $i <=8 && $j>=1 && $j<=8) {
		$sA = ">!<";
		$z1 = $i;
		$z2 = $j;
		&string_compare;
		
		if($z3 == 1) {
		    $d0 = 1;
		    $sC = "DOCKED";
		    $e=$e0;
		    $p=$p0;
		    print "Shields dropped for docking purposes.\n";
		    $s=0;
		}
	    }
	}
    }

    if ($d[2] < 0) {
	print "\n*** Short Range Sensors are out ***\n";
	return;
    }

    print "------------------------\n";
    for ($i=0;$i<8;$i++) {
	print substr($sQ,$i*24,24);
#$temp =	 substr($sQ,$i*24,24);
#$temp =~ s/ /./g;
#print $temp;
	if ($i == 0) {
	    printf("    Stardate            %d\n", $t);
	}
	elsif ($i == 1) {
	    printf("    Condition           %s\n", $sC);
	}
	elsif ($i == 2) {
	    printf("    Quadrant            %d, %d\n", $q1, $q2);
	}
	elsif ($i == 3) {
	    printf("    Sector              %d, %d\n",int($s1+.5),int($s2+.5));
	}
	elsif ($i == 4) {
	    printf("    Photon Torpedoes    %d\n", $p);
	}
	elsif ($i == 5) {
	    printf("    Total Energy        %d\n", $e + $s);
	}
	elsif ($i == 6) {
	    printf("    Shields             %d\n", $s);
	}
	elsif ($i == 7) {
	    printf("    Klingons Remaining  %d\n", $k9);
	}
    }
    printf("------------------------\n\n");

}

sub long_range_scan {
    if ($d[3] < 0) {
	print "Long Range Sensors are inoperable.\n";
	return;
    }

    printf("Long Range Scan for Quadrant %d, %d\n\n", $q1, $q2);

    for ($i=$q1-1;$i<=$q1+1;$i++) {
	print "--------------------\n";
	for ($j=$q2-1;$j<=$q2+1;$j++) {
	    if ($i>0 && $i<=8 && $j>0 && $j<=8) {
		$z[$i][$j] = $g[$i][$j];
		printf(" %3.3d :",$z[$i][$j]);
	    }
	    else {
		print " *** :";
	    }
	}
	print "\n";
    }
    print "--------------------\n\n";
}

sub phaser_control {

    if (!$data{units}) {
	if ($d[4] < 0.0) {
	    printf("Phasers Inoperative\n\n");
	    return;
	}
	
	if ($k3 <= 0) {
	    printf("Science Officer Spock reports:\n");
	    printf("  'Sensors show no enemy ships in this quadrant'\n\n");
	    return;
	}
	
	if ($d[8] < 0.0) {
	    printf("Computer failure hampers accuracy.\n");
	}
	
	printf("Phasers locked on target;\n");
	printf("Energy available = %d units\n\n", $e);
	print "<form action=trek.cgi method=post>";
	printf("Number of units to fire: ");
	
	$give_command = 0;
	$state=&encode($state);
	print "<input type=hidden name=state value=\"$state\">";
	print "<input type=hidden name=command value=pha>";
       	print "<input type=text size=4 name=units><p>\n";
	print "<input type=submit value=Fire></form>";
    }
    else {

	$iEnergy = $data{units};
	
	if ($iEnergy <= 0) {
	    return;
	}
	if ($e - $iEnergy < 0) {
	    printf("Not enough energy available.\n\n");
	    return;
	}

	$e = $e - $iEnergy;
	
	if ($d[8] < 0.0) {
	    $iEnergy = $iEnergy * rand();
	}
	
	$h1 = $iEnergy / $k3;
	
	for ($i = 1; $i <= 3; $i++) {
	    if ($k[$i][3] > 0) {
		$h = ($h1 / &function_d(0) * (rand() + 2));
		if ($h <= .15 * $k[$i][3]) {
		    printf("Sensors show no damage to enemy at ");
		    printf("%d, %d\n\n", $k[$i][1], $k[$i][2]);
		}
		else {
		    $k[$i][3] = $k[$i][3] - $h;
		    printf("%d unit hit on Klingon at sector ", $h);
		    printf("%d, %d\n", $k[$i][1], $k[$i][2]);
		    if ($k[$i][3] <= 0) {
			printf("*** Klingon Destroyed ***\n\n");
			$k3--;
			$k9--;
			$z1 = $k[$i][1];
			$z2 = $k[$i][2];
			$sA = "   ";
			&insert_in_quadrant;
			$k[$i][3] = 0;
			$g[$q1][$q2] = $g[$q1][$q2] - 100;
			$z[$q1][$q2] = $g[$q1][$q2];
			if ($k9 <= 0) {
			    &won_game;
			}
		    }
		    else {
			printf("\n");
		    }
		}
	    }
	}
	
	&klingons_shoot;

    }
}

sub photon_torpedoes {

    if (!$data{course}) {
	if ($p <= 0) {
	    printf("All photon torpedoes expended\n");
	    return;
	}
	
	if ($d[5] < 0.0) {
	    printf("Photon Tubes not operational\n");
	    return;
	}

	print "<form action=trek.cgi method=post>";
	
	printf("Course (0-9): ");
	
	$give_command = 0;
	$state=&encode($state);
	print "<input type=hidden name=state value=\"$state\">";
	print "<input type=hidden name=command value=tor>";
	print "<input type=text name=course size=4><p>\n";
	print "<input type=submit value=Fire></form>";

    }
    else {

	$c1 = $data{course};
	
	$c1 = 1.0 if ($c1 == 9.0);

	if ($c1 < 0 || $c1 > 9.0) {
	    printf("Ensign Chekov roports:\n");
	    printf("  Incorrect course data, sir!\n\n");
	    return;
	}
	
	$e = $e - 2;
	$p--;
	
	$c2 = int($c1+.5);
	$c3 = $c2 + 1;
	
	$x1 = $c[0][$c2] + ($c[0][$c3] - $c[0][$c2]) * ($c1 - $c2);
	$x2 = $c[1][$c2] + ($c[1][$c3] - $c[1][$c2]) * ($c1 - $c2);
	
	$x = $s1 + $x1;
	$y = $s2 + $x2;
	
	$x3 = int($x+.5);
	$y3 = int($y+.5);
	
	$x5 = 0;
	
	printf("Torpedo Track:\n");
#	print "X1: $x1 X2: $x2 X: $x Y: $y\n";
	while ($x3 >= 1 && $x3 <= 8 && $y3 >= 1 && $y3 <= 8) {
	    printf("    %d, %d\n", $x3, $y3);
	    
	    $sA = "   ";
	    $z1 = $x3;
	    $z2 = $y3;
	    
	    &string_compare;
	    
	    if ($z3 == 0) {
#		print "HIT!\n";
		&torpedo_hit;
		&klingons_shoot;
		return;
	    }
	    
	    $x = $x + $x1;
	    $y = $y + $x2;
	    
	    $x3 = int($x+.5);
	    $y3 = int($y+.5);
	}
	
	printf("Torpedo Missed\n\n");
	
	&klingons_shoot;
    }
}

sub torpedo_hit {
    $x3 = int($x+.5);
    $y3 = int($y+.5);

    $z3 = 0;

    $sA = " * ";
    $string_compare;

    if ($z3 == 1) {
	printf("Star at %d, %d absorbed torpedo energy.\n\n", $x3, $y3);
	return;
    }

    $sA = "+K+";
    &string_compare;

    if ($z3 == 1) {
	printf("*** Klingon Destroyed ***\n\n");
	$k3--;
	$k9--;

	if ($k9 <= 0) {
	    &won_game;
	}
	
	for ($i=0; $i<=3; $i++) {
	    if ($x3 == $k[$i][1] && $y3 == $k[$i][2]) {
		$k[$i][3] = 0;
	    }
	}
    }

    $sA = ">!<";
    &string_compare;

    if ($z3 == 1) {
	printf("*** Starbase Destroyed ***\n");
	$b3--;
	$b9--;
	
	if ($b9 <= 0 && $k9 <= $t - $t0 - $t9) {
	    printf("That does it, Captain!!");
	    printf("You are hereby relieved of command\n");
	    printf("and sentanced to 99 stardates of hard");
	    printf("labor on Cygnus 12!!\n");
	    &resign_commision;
        }
	
	printf("Starfleet Command reviewing your record to consider\n");
	printf("court martial!\n\n");
	
	$d0 = 0;    # Undock 
    }
    
    $z1 = $x3;
    $z2 = $y3;
    $sA = "   ";
    &insert_in_quadrant;

    $g[$q1][$q2] = ($k3 * 100) + ($b3 * 10) + $s3;
    $z[$q1][$q2] = $g[$q1][$q2];

}

sub damage_control {
    $d3 = 0.0;

    if ($d[6] < 0.0) {
	printf("Damage Control report not available.\n");
    }
    elsif (!$data{repairok}) {
	printf("Device            State of Repair\n");
	
	for ($r1 = 1; $r1 <= 8; $r1++) {
	    &get_device_name;
	    printf($sG2);
	    for ($i = 1; $i < 25 - length($sG2); $i++) {
		printf(" ");
	    }
	    printf("%4.1f\n", $d[$r1]);
	}
	
	printf("\n");
    }

    if ($d0 == 0) {
	return;
    }
    
    if (!$data{repairok}) {
	$d3 = 0.0;
	for ($i = 1; $i <= 8; $i++) {
	    if ($d[$i] < 0.0) {
		$d3 = $d3 + .1;
	    }
	}
	
	if ($d3 == 0.0) {
	    return;
	}
	
	$d3 = $d3 + $d4;
	if ($d3 >= 1.0) {
	    $d3 = 0.9;
	}
	
	printf("\nTechnicians standing by to effect repairs to your\n");
	printf("ship; Will you authorize the repair order (Y/N)?<p>\n");
	print "<form action=trek.cgi method=post>";
	$statenc = &encode($state);
	print "<input type=hidden name=state value=\"$statenc\">";
	print "<input type=hidden name=command value=dam>";
	print "<input type=hidden name=repairok value=1>";
	print "<input type=submit value=OK></form><p>\n";
    }
    
    else {
	for ($i = 1; $i <= 8; $i++) {
	    if ($d[$i] < 0.0) {
		$d[$i] = 0.0;
	    }
	}
	
	$t = $t + $d3 + 0.1;

	printf("Device            State of Repair\n");
	
	for ($r1 = 1; $r1 <= 8; $r1++) {
	    &get_device_name;
	    printf($sG2);
	    for ($i = 1; $i < 25 - length($sG2); $i++) {
		printf(" ");
	    }
	    printf("%4.1f\n", $d[$r1]);
	}
	
	printf("\n");

    }
    
}

sub sheild_control {

    if (!$data{units}) {
	if ($d[7] < 0.0) {
	    printf("Sheild Control inoperable\n");
	    return;
	}
	
	printf("Energy available = %d\n\n", $e + $s);
	
	print "<form action=trek.cgi method=post>";
	printf("Input number of units to sheilds: ");
	
	$give_command = 0;
	$state=&encode($state);
	print "<input type=hidden name=state value=\"$state\">";
	print "<input type=hidden name=command value=she>";
	print "<input type=text size=5 name=units><p>\n";
	print "<input type=submit value=Change>";
    }
    else {
	$i = $data{units};
	
	if ($i < 0 || $s == $i) {
	    printf("<Shields Unchanged>\n\n");
	    return;
	}
	
	if ($i >= $e + $s) {
	    printf("Sheild Control Reports:\n");
	    printf("  'This is not the Federation Treasury.'\n");
	    printf("<Sheilds Unchanged>\n\n");
	    return;
	}
	
	$e = $e + $s - $i;
	$s = $i;
	
	printf("Deflector Control Room report:\n");
	printf("  'Shields now at %d units per your command.'\n\n", $s);
    }
}

sub library_computer {
    if ($d[8] < 0) {
	print "Library Computer inoperable\n";
	return;
    }
    
    if (!$data{function}) {
	$give_command = 0;
	$state=&encode($state);
	print "Computer active and awaiting command: \n\n";
	print "<p><form action=trek.cgi method=post>";
	print "<input type=hidden name=state value=\"$state\">";
	print "<input type=hidden name=command value=com>";
	print "<select name=function>";
	print "<option value=9>Cumulative Galactic Record";
	print "<option value=1>Status Report";
	print "<option value=2>Photon Torpedo Data";
	print "<option value=3>Starbase Nav Data";
	print "<option value=4>Direction/Distance Calculator";
	print "<option value=5>Galaxy 'Region Name' Map";
	print "</select><input type=submit value=Enter>";
	print "</form>";
    }
    else {
	&galactic_record if ($data{function} == 9);
	&status_report if ($data{function} == 1);
	&torpedo_data if ($data{function} == 2);
	&nav_data if ($data{function} == 3);
	&dirdist_calc if ($data{function} == 4);
	&galaxy_map if ($data{function} == 5);
    }
}

sub galactic_record {
    printf("\n     Computer Record of Galaxy for Quadrant %d,%d\n\n",$q1,$q2);
    printf("     1     2     3     4     5     6     7     8\n");

    for ($i = 1; $i <= 8; $i++)  {
	printf("   ----- ----- ----- ----- ----- ----- ----- -----\n");

	printf("%d", $i);

	for ($j = 1; $j <= 8; $j++)  {
	    printf("   ");

	    if ($z[$i][$j] == 0) {
		printf("***");
	    }
	    else {
		printf("%3.3d", $z[$i][$j]);
	    }
	}
	
	printf("\n");
    }

    printf("   ----- ----- ----- ----- ----- ----- ----- -----\n\n");
    
}

sub status_report {
    $sX = ($k9>1)?"s":"";
    printf ("     Status Report:\n\n");
    printf("Klingon%s Left: %d\n", $sX, $k9);
    printf("Mission must be completed in %4.1f stardates\n",
	   (10*($t0+$t9-$t))/10);
    if ($b9<1) {
	print "Your stupidity has left you on your own in the galaxy\n";
	print " -- you have no starbases left!\n\n";
    }
    else {
	$sX = ($b9<2)?"":"s";
	printf("The Federation is maintaining %d starbase%s in the galaxy.\n\n", $b9,$sX);
    }
}

sub torpedo_data {
    $sX = "";

    if ($k3 <= 0) {
	printf("Science Officer Spock reports:\n");
	printf("  'Sensors show no enemy ships in this quadrant.'\n\n");
	return;
    }

    $sX = "s" if ($k3 > 1);
 
    printf("From Enterprise to Klingon battlecriuser%s:\n\n", $sX);

    for ($i = 1; $i <= 3; $i++) {
	if ($k[$i][3] > 0) {
	    $w1 = $k[$i][1];
	    $x  = $k[$i][2];
	    $c1 = $s1;
	    $a  = $s2;
	    
	    &compute_vector;
	}
    }

}

sub nav_data {
    if ($b3 <= 0) {
	printf("Mr. Spock reports,\n");
	printf("  'Sensors show no starbases in this quadrant.'\n\n");
	return;
    }

    $w1 = $b4;
    $x  = $b5;
    $c1 = $s1;
    $a  = $s2;

    &compute_vector;
}

sub dirdist_calc {
    if (!$data{x1}) {
	printf("Direction/Distance Calculator\n\n");
	
	printf("You are at quadrant %d,%d sector %d,%d\n\n", $q1, $q2,
	       int($s1+.5), int($s2+.5));
	
	$give_command = 0;
	$state=&encode($state);

	print "<form action=trek.cgi method=post>";
	print "<input type=hidden name=state value=\"$state\">";
	print "<input type=hidden name=command value=com>";
	print "<input type=hidden name=function value=4>";
	printf("Please enter initial X coordinate: ");
	print "<input type=text name=x1 size=2><p>\n";
	printf("Please enter initial Y coordinate: ");
	print "<input type=text name=y1 size=2><p>\n";
	printf("Please enter final X coordinate: ");
	print "<input type=text name=x2 size=2><p>\n";
	printf("Please enter final Y coordinate: ");
	print "<input type=text name=y2 size=2><p>\n";
	print "<input type=submit value=Enter></form>";
    }
    else {
	
	$c1 = $data{x1};
	$a = $data{y1};
	$w1 = $data{x2};
	$x = $data{y2};

	&compute_vector;
    }
}

sub galaxy_map {
    $g5 = 1;

    printf("\n                   The Galaxy\n\n");
    printf("    1     2     3     4     5     6     7     8\n");

    for ($i = 1; $i <= 8; $i++) {
	printf("  ----- ----- ----- ----- ----- ----- ----- -----\n");
	
	printf("%d ", $i);

	$z4 = $i;
	$z5 = $1;
	&quadrant_name;

	$j0 = int(11 - (length($sG2) / 2));

	for ($j = 0; $j < $j0; $j++) {
	    printf(" ");
	}

	printf($sG2);

	for ($j = 0; $j < $j0; $j++) {
	    printf(" ");
	}

	if (! (length($sG2) % 2)) {
	    printf(" ");
	}

	$z5 = 5;
	&quadrant_name;

	$j0 = int(12 - (length($sG2) / 2));

	for ($j = 0; $j < $j0; $j++) {
	    printf(" ");
	}

	printf($sG2); 
   
	printf("\n");
    }
    
    printf("  ----- ----- ----- ----- ----- ----- ----- -----\n\n");
    
}

sub compute_vector {
    $x = $x - $a;
    $a = $c1 - $w1;

    if ($x <= 0.0) {
	if ($a > 0.0) {    
	    $c1 = 3.0;
	    &sub2;
	    return;
	}
	else {
	    $c1 = 5.0;
	    &sub1;
	    return;
	}
    }
    elsif ($a < 0.0) {
	$c1 = 7.0;
	&sub2;
	return;
    }
    else {
	$c1 = 1.0;
	&sub1;
	return;
    }
}

sub sub1 {
    $x = abs($x);
    $a = abs($a);
    
    if ($a <= $x) {
	printf("  DIRECTION = %4.2f\n", $c1 + ($a / $x));
    }
    else {
	printf("  DIRECTION = %4.2f\n", $c1 + ((($a * 2) - $x) / $a));
    }
    
    printf("  DISTANCE = %4.2f\n\n", ($x > $a) ? $x : $a);
    
}

sub sub2 {
    $x = abs($x);
    $a = abs($a);
    
    if ($a >= $x) {
	printf("  DIRECTION = %4.2f\n", $c1 + ($x / $a));
    }
    else {
	printf("  DIRECTION = %4.2f\n\n", $c1 + ((($x * 2) - $a) / $x));
    }
    
    printf("  DISTANCE = %4.2f\n", ($x > $a) ? $x : $a);
    
}

sub ship_destroyed {
    printf("The Enterprise has been destroyed. ");
    printf("The Federation will be conquered.\n\n");
    
    &end_of_time;
}

sub end_of_time {
    printf("It is stardate %d.\n\n", $t);
    
    &resign_commision;
}

sub resign_commision {
    printf("There were %d Klingon Battlecruisers left at the", $k9);
    printf(" end of your mission.\n\n");
    
    &end_of_game;
}

sub won_game {
    printf("Congradulations, Captain!  The last Klingon Battle Cruiser\n");
    printf("menacing the Federation has been destoyed.\n\n");
    
    printf("Your efficiency rating is %4.2f\n", 1000*(($k7/($t-$t0))**2))
	if (($t - $t0) > 0);
    &end_of_game;
}

sub end_of_game {
    
    if ($b9 > 0)  {
	printf("The Federation is in need of a new starship commander");
	printf(" for a similar mission.\n");
	printf("If there is a volunteer, let him step forward and");
	printf(" enter '<a href=trek.cgi onmouseover=\"status='Start a New Game';return true\">aye</a>'.\n ");
    }
    
    exit;
}

sub klingons_move {

    for ($i = 1; $i <= 3; $i++) {
	if ($k[$i][3] > 0) {
	    $sA = "   ";
	    $z1 = $k[$i][1];
	    $z2 = $k[$i][2];
	    &insert_in_quadrant;

	    &find_empty_place;
	    
	    $k[$i][1] = $z1;
	    $k[$i][2] = $z2;
	    $sA = "+K+";
	    &insert_in_quadrant;
        }
    }

    &klingons_shoot;

}

sub klingons_shoot {

    if ($k3 <= 0) {
	return;
    }

    if ($d0 != 0) {
	printf("Starbase shields protect the Enterprise\n\n");
	return;
    }

    for ($i = 1; $i <= 3; $i++) {
	if ($k[$i][3] > 0) {
	    $h = int(($k[$i][3] / &function_d($i)) * (2 + rand()));
	    $s = $s - $h;
	    $k[$i][3] = $k[$i][3] / (3 + rand());

	    printf("%d unit hit on Enterprise from sector ", $h);
	    printf("%d, %d\n", $k[$i][1], $k[$i][2]);
 
	    if ($s <= 0) {
		printf("\n");
		&ship_destroyed;
            }
	    
	    printf("    <Shields down to %d units>\n\n", $s);

	    if ($h >= 20) {
		if (rand() <= 0.6 || ($h / $s) > 0.2) {
		    $r1 = int(rand(8)+1);
		    $d[$r1] = $d[$r1] - ($h / $s) - (0.5 * rand());
		    
		    &get_device_name;
		    
		    printf("Damage Control reports\n");
		    printf("   '%s' damaged by hit\n\n", $sG2);
                }
	    }
        }
    }
    
}

sub repair_damage {

    $d6 = $w1;

    if ($w1 >= 1.0) {
	$d6 = $w1 / 10;
    }

    for ($i = 1; $i <= 8; $i++) {
	if ($d[$i] < 0.0) {
	    $d[$i] = $d[$i] + $d6;
	    if ($d[$i] > -0.1 && $d[$i] < 0) {
		$d[$i] = -0.1;
	    }
	    elsif ($d[$i] >= 0.0) {
		if ($d1 != 1) {
		    $d1 = 1;
		}

		printf("Damage Control report:\n");
		$r1 = $i;
		&get_device_name;
		printf("    %s repair completed\n\n", $sG2);
            }
        }
    }

    if (rand() <= 0.2) {
	$r1 = int(rand(8)+1);

	if (rand() < .6) {
	    $d[$r1] = $d[$r1] - (rand() * 5.0 + 1.0);
	    printf("Damage Control report:\n");
	    &get_device_name;
	    printf("    %s damaged\n\n", $sG2);
        }
	else {
	    $d[$r1] = $d[$r1] + (rand() * 3.0 + 1.0);
	    printf("Damage Control report:\n");
	    &get_device_name;
	    printf("    %s state of repair improved\n\n", $sG2);
        }
    }
    
}

sub find_empty_place {
    while ($z3 == 0) {
	$r1=int(rand(8)+1);
	$r2=int(rand(8)+1);
	$sA = "   ";
	$z1=$r1;
	$z2=$r2;
	&string_compare;
    }
    $z3=0;
}

sub insert_in_quadrant {

    $s8=(($z2-1)*3)+(($z1-1)*24)+1;

#    print "IIC - $sA - LEN: ".length($sQ)." S8: $s8 Z2: $z2 Z1: $z1\n";
    substr($sQ,$s8-1,3)=$sA;

}

sub get_device_name {
    $r1 = 0 if ($r1<0 || $r1>8);
    $sG2 = $device_name[$r1];
}

sub string_compare {
    $s8=(($z2-1)*3)+(($z1-1)*24) + 1;
    $z3=(substr($sQ,$s8-1,3) eq $sA)?1:0;
#    print "SCOMP:".substr($sQ,$s8-1,3).":".$sA.": S8: $s8 Z1: $z1 Z2: $z2 Z3: $z3\n";
}

sub quadrant_name {
    if ($z4<1 || $z4>8 || $z5<1 || $z5>8) {
	$sG2 = "Unknown";
    }
    if ($z5 <=4) {
	$sG2 = $quad_name[$z4];
    }
    else {
	$sG2 = $quad_name[$z4+8];
    }
    if ($g5 != 1) {
	if ($z5 > 4) {
	    $z5 -=4;
	}
	$sG2 .= $sect_name[$z5];
    }
}

sub function_d {
    my $i = shift;

    $j = sqrt((($k[$i][1] - $s1)**2) + (($k[$i][2] - $s2)**2));

    return $j;
}











sub parse {
    my $state = shift;

    ($b3,$b4,$b5,$b9,$d0,$d1,$e,$k3,$k7,$k9,$p,
     $q1,$q2,$s,$s3,$t0,$t9,$sQstate,$tpack,$s1pack,$s2pack,
     $galstate,$klingstate,$damstate,$w1pack,$zstate) = 
	 unpack("AAAAAAA4AA2A2A2AAA4A2A4A2A64A8A3A3A192A27A54A3A192",$state);

    $t = $tpack/10000;
    $s1 = $s1pack/100;
    $s2 = $s2pack/100;
    $w1 = $w1pack/100;

    for ($i=1;$i<=8;$i++) {
        for ($j=1;$j<=8;$j++) {
	    $g[$i][$j] = substr($galstate,(($i-1)*24+($j-1)*3),3);
	}
    }

    for ($i=1;$i<=8;$i++) {
        for ($j=1;$j<=8;$j++) {
	    $z[$i][$j] = substr($zstate,(($i-1)*24+($j-1)*3),3);
	}
    }

    for ($i=1;$i<=3;$i++) {
        for ($j=1;$j<=3;$j++) {
	    $k[$i][$j] = substr($klingstate,(($i-1)*9+($j-1)*3),3);
	}
    }

    $sQ = "";
    for ($i=0;$i<64;$i++) {
	$sQbit = substr($sQstate,$i,1);
	$addit = "   ";
        $addit = " * " if ($sQbit eq "1");
        $addit = "<*>" if ($sQbit eq "2");
        $addit = "+K+" if ($sQbit eq "3");
        $addit = ">!<" if ($sQbit eq "4");
        $sQ .= $addit;
    }
    $sQ .= " ";

    for ($i=0;$i<=8;$i++) {
	$dampack = substr($damstate,($i*6),6);
	$d[$i] = $dampack/100;
    }
}

sub esrap {

    $galstate = "";
    for ($i=1;$i<=8;$i++) {
	for ($j=1;$j<=8;$j++) {
	    $galbit = 0;
	    $galbit = sprintf("%03d",$g[$i][$j]);
	    $galstate.=$galbit;
	}
    }

    $zstate = "";
    for ($i=1;$i<=8;$i++) {
	for ($j=1;$j<=8;$j++) {
	    $zbit = 0;
	    $zbit = sprintf("%03d",$z[$i][$j]);
	    $zstate.=$zbit;
	}
    }

    $klingstate = "";
    for ($i=1;$i<=3;$i++) {
        for ($j=1;$j<=3;$j++) {
	    $klingbit = sprintf("%03d",$k[$i][$j]);
	    $klingstate .= $klingbit;
	}
    }
    
    $sQstate = "";
    for ($i=0;$i<64;$i++) {
	$sQbit = substr($sQ,($i*3),3);
	$addit = 0;
	$addit = 1 if ($sQbit eq " * ");
	$addit = 2 if ($sQbit eq "<*>");
	$addit = 3 if ($sQbit eq "+K+");
	$addit = 4 if ($sQbit eq ">!<");
	$sQstate .= $addit;
    }

    $damstate = "";
    for ($i=0;$i<=8;$i++) {
	$dampack = $d[$i] * 100;
	$dambit = sprintf("%06d",$dampack);
	$damstate .= $dambit;
    }

    $tpack = int($t*10000);
    $s1pack = int($s1*100);
    $s2pack = int($s2*100);
    $w1pack = int($w1*100);

    $state = sprintf("%01d%01d%01d%01d%01d%01d%04d%01d%02d%02d%02d%01d%01d%04d%02d%04d%02d%064s%08d%03d%03d%0192s%027s%054s%03d%0192s",
		     $b3,$b4,$b5,$b9,$d0,$d1,$e,$k3,$k7,$k9,$p,
		     $q1,$q2,$s,$s3,$t0,$t9,$sQstate,$tpack,$s1pack,$s2pack,
		     $galstate,$klingstate,$damstate,$w1pack,$zstate);

    $state =~ s/ /0/g;

    return $state;
}


sub encode {
    my $state = shift;

    chomp $state;
    my $key = int(rand(length($codestring)));
    my $string = substr($codestring,$key,length($codestring)) . 
	substr($codestring,0,$key);

    eval "\$state =~ tr/0-9a-zA-Z/$string/";
    $state = substr($codestring,$key,1).$state;

    return $state;
    
}

sub decode {

    my $state = shift;
    my $key;
    chomp $state;
    ($key,$state) = ($state =~ /^(.)(.*)$/);

    $codestring =~ m/$key/g;

    $key = (pos $codestring) - 1;

    my $string = substr($codestring,$key,length($codestring)) .
        substr($codestring,0,$key);

    eval "\$state =~ tr/$string/0-9a-zA-Z/";

    return $state;
}

