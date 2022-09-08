#!/usr/bin/perl
 
use strict;
use warnings;
use threads;
use Thread::Queue;

sub pipeCommand {
    my $cmd = shift;
    my $Q = new Thread::Queue;
    async{
        my $pid = open my $pipe, $cmd or die $!;
        $Q->enqueue( $_ ) while <$pipe>;
        $Q->enqueue( undef );
    }->detach;
    return $Q;
}

my $pipe = pipeCommand(
    'DISPLAY=:0 xscreensaver-command -watch |'
) or die;

print_("Starting, waiting on input.\n");
while( 1 ) {
    if( $pipe->pending ) {
        my $line = $pipe->dequeue or last;
        print_("$line");
		if ($line =~ m/^(BLANK|LOCK)/) {
			`vcgencmd display_power 0`
 		}
        elsif ($line =~ m/^UNBLANK/) {
            `vcgencmd display_power 1`
        }
    }
}

sub print_{
	print "[".localtime(time) .  "] @_";
}
