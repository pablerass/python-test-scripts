#!/usr/bin/perl
##########################################################
# Script: send-mail.pl
# Desc: Script de envío de correos.
# Revisions:
#	20150420 - pmunoz - Primera versión del script.
##########################################################

use warnings;
use strict;

sub send_mail {
	# from - string
	# to - string o string[]
	# cc - string o string[]
	# bcc - string o string[]
	# subject - string
	# body - string
	# debig - integer

    my %args = (
        from => 'test.mail@test.ma',
        to => '',
        cc => '',
        bcc => '',
        subject => '',
        body => '',
		debug => 0,
        @_);

    # Convert to, cc, bcc parameters into lists
    my @to;
    my @cc;
    my @bcc;
    if (ref($args{to}) eq 'ARRAY') {
	@to = @{$args{to}};
    } else {
        @to = ($args{to});
    }

    if (ref($args{cc}) eq 'ARRAY') {
	@cc = @{$args{cc}};
    } else {
        @cc = ($args{cc});
    }

    if (ref($args{bcc}) eq 'ARRAY') {
	@bcc = @{$args{bcc}};
    } else {
        @bcc = ($args{bcc});
    }

    # Create SMTP client
    use Net::SMTP;

    # SMTP parameters
    my $smtp_server = 'smtp.test.ma';
    my $smtp_port = 25;
    my $smtp_user = '';
    my $smtp_password = '';
    my $smtp_debug = $args{debug};

    # Connect to SMTP server
    my $smtp = Net::SMTP->new($smtp_server, Port => $smtp_port,
			      Timeout => 10, Debug => $smtp_debug);
    die "Could not connect to server $smtp_server\n" unless $smtp;
    $smtp->auth($smtp_server, $smtp_password) unless $smtp_user eq '';

    # Send mail
    $smtp->mail($args{from});
    $smtp->to(@to) unless $args{to} eq '';
    $smtp->cc(@cc) unless $args{cc} eq '';
    $smtp->bcc(@bcc) unless $args{bcc} eq '';
    $smtp->data;
    $smtp->datasend("Content-Type: text/plain; charset=UTF-8\n");
    $smtp->datasend("From: $args{from}\n");
    $smtp->datasend("To: ", join(', ', @to), "\n") unless $args{to} eq '';
    $smtp->datasend("Cc: ", join(', ', @cc), "\n") unless $args{cc} eq '';
    $smtp->datasend("Bcc: ", join(', ', @bcc), "\n") unless $args{bcc} eq '';
    $smtp->datasend("Subject: $args{subject}\n") unless $args{subject} eq '';
    $smtp->datasend("\n");
    $smtp->datasend("$args{body}\n") unless $args{body} eq '';
    $smtp->dataend;

    # Close STMP connection
    $smtp->quit;
}

send_mail(cc => ['dest1@dest.ma', 'dest2@dest,ma'],
          bcc => 'dest3@dest.ma',
          subject => 'Correo de prueba',
          body => 'Esto no es más que un correo de prueba');
