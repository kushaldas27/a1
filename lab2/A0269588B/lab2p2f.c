#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <fcntl.h>

int main() {

    printf("Be patient, the program will take around 7 seconds to run.\n");
    printf("At the end you can do \"cat results.out\" to see the result.\n");

    //
    // Add code here to pipe from ./slow “This is a test sentence” to ./talk and redirect
    // output of ./talk to results.out
    // I.e. your program should do the equivalent of ./slow “This is a test sentence” | ./talk > results.out
    // WITHOUT using | and > from the shell.
    //
    // pipe -> exec
    // ./slow writes
    // ./talk reads

    int p[2];

    // This creates a pipe. p[0] is the reading end,
    // p[1] is the writing end.
    if(pipe(p) < 0) 
        perror("lab2p2f: ");

    if (fork() != 0) {
        // Parent process reads output of ./slow from child 
        // Put reading end into stdin
        // Run ./talk
        // Redirect output of ./talk into results.out
        close(p[1]);
        
        int fp_out = open("./results.out", O_CREAT | O_WRONLY, 0666);
        dup2(p[0], STDIN_FILENO);
        dup2(fp_out, STDOUT_FILENO);
        execl("./talk", "talk", (char *) 0);
        
        close(p[0]);
        close(fp_out);
    } else {
        // Child process runs ./slow
        // Put stdout into writing end
        close(p[0]);
        dup2(p[1], STDOUT_FILENO);
        execlp("./slow", "slow", "This is a test sentence", NULL);
        close(p[1]); 
        exit(0);
    }
}
