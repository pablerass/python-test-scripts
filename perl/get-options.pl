#!/usr/bin/perl

use strict;
use warnings;

use Getopt::Long qw(GetOptions);

my $dry_run = 0;
my $conf_file;
my @warn_mail = ();

GetOptions(
		'conf-file=s' => \$conf_file,
		'warn-mail=s' => \@warn_mail,
		'dry-run' => \$dry_run
) or die "Usage: $0 --conf-file <file> [--warn-mail <mail>] [--dry-run]";

@warn_mail = split(/,/,join(',',@warn_mail));

if ($dry_run) {
	print 'dry-run';
} else {
	print 'no dry-run';
}

if ($conf_file) {
	print $conf_file;
}
if (@warn_mail) {
	print join(", ", @warn_mail);
}
