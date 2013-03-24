#!/usr/bin/perl -w
%currentVals = ();
%totalVals = ();

sub outputcsv {
  @d = split(/\//, $currentdate);
  $year = $d[2];
  $month = sprintf("%02d", $d[1]);
  $day   = sprintf("%02d", $d[0]);
  $filename = "13 Cow Lane-$year$month$day.csv";
  open(OUTFILE, "> $filename");
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
        if ( scalar keys %currentVals > 1 ) {
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


