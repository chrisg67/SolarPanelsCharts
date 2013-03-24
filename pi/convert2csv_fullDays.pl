#!/usr/bin/perl -w
%currentVals = ();
%totalVals = ();
@shortMonths = ( "01 - Jan", "02 - Feb", "03 - Mar", "04 - Apr", "05 - May", "06 - Jun",
                 "07 - Jul", "08 - Aug", "09 - Sep", "10 - Oct", "11 - Nov", "12 - Dec" );

sub outputcsv {
  @d = split(/\//, $currentdate);
  $year = $d[2];
  $month = sprintf("%02d", $d[1]);
  $day   = sprintf("%02d", $d[0]);
  $filename = "13 Cow Lane-$year$month$day.csv";
  $dir = $shortMonths[$d[1]-1];
  unless ( -d $dir ) {
    mkdir $dir;
  }
  open(OUTFILE, "> $dir/$filename");
  @keys = (sort keys(%currentVals));
  foreach my $key (@keys) {
    print OUTFILE "$currentdate $key;";
    print OUTFILE $totalVals{$key};
    print OUTFILE ";";
    print OUTFILE $currentVals{$key};
    print OUTFILE "\n";
  }
  close OUTFILE;
}

$currentdate="";
while (<>) {
  chop;
  if ( /\d+\/\d+\/\d+ \d+:\d+:\d+/ ) {
    @vals = split(/ +/, $_);
    my $date = $vals[0];
    my $time = $vals[1];
    my $total = $vals[2];
    $total =~ s/total=//;
    # KWh = $vals[3];
    my $current = $vals[4];
    $current =~ s/current=//;

    if ( $date ne $currentdate ) {
      if ( $currentdate ) {
        if ( scalar keys %currentVals == 288 ) {
          outputcsv();
        }
      }
      $currentdate = $date;
      %currentVals = ();
      %totalVals = ();
    }

    $currentVals{$time} = $current/1000;
    $totalVals{$time} = $total;
  }
}

outputcsv();


