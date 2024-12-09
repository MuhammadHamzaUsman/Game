#include<stdio.h>
#include<conio.h>
void game()
{
    char table[9] = {'1','2','3','4','5','6','7','8','9'}, s = 'X';
    int p = 1,t;
    printf("\n\n\n\n\n\n\t\t\t\t\"TICKCROSS\"\n\t\t\t\t %c | %c | %c\n\t\t\t\t---+---+---\n\t\t\t\t %c | %c | %c\n\t\t\t\t---+---+---\n\t\t\t\t %c | %c | %c\n", table[0], table[1], table[2], table[3], table[4], table[5], table[6], table[7], table[8]);
    for(int i=1;i<=9;i++)
    {
        printf("\t\t\t Enter choice player %d (%c) : ", p, s);
        scanf("%d", &t);
        if(table[t-1]=='X'||table[t-1]=='O'||t>9)
        {
            printf("\t\t\t\tInvalid choice\n");
        }
        else
        {
            system("cls");
            if(p==1)
            {
                p++ , table[t-1] = 'X' , s = 'O';
            }
            else if (p==2)
            {
                p-- , table[t-1] = 'O' , s = 'X';
            }
            printf("\n\n\n\n\n\n\t\t\t\t\"TICKCROSS\"\n\t\t\t\t %c | %c | %c\n\t\t\t\t---+---+---\n\t\t\t\t %c | %c | %c\n\t\t\t\t---+---+---\n\t\t\t\t %c | %c | %c\n", table[0], table[1], table[2], table[3], table[4], table[5], table[6], table[7], table[8]);
            if(table[0]==table[1]&&table[1]==table[2]||table[3]==table[4]&&table[4]==table[5]||table[6]==table[7]&&table[7]==table[8]||table[1]==table[4]&&table[4]==table[7]||table[2]==table[5]&&table[5]==table[8]||table[0]==table[4]&&table[4]==table[8]||table[2]==table[4]&&table[4]==table[6]||table[0]==table[3]&&table[3]==table[6])
            {
                printf("\t\t\t\tPLAYER %d WON\n\t\t\t PRESS ENTER FOR MAIN MENUE",p-1);
                i=9;
            }
            else if(i>8)
            {
                printf("\t\t\t\t    DRAW\n\t\t\t PRESS ANY KEY FOR MAIN MENUE");
            }
        }
    }
}
void main()
{
    char c;
    for(int i = 0 ; i <= 1; i--)
    {
        printf("\n\n\n\n\n\n\t\t\t\t\"TICKCROSS\"\n\t\t\t       START GAME : S\n\t\t\t\tTUTORIAL : T\n\t\t\t\t  QUIT : Q\n\t\t\t       ENTER CHOICE : ");
        scanf("%c", &c);
        if(c=='S')
        {
            system("cls");
            game();
            getch();
        }
        else if(c=='T')
        {
            system("cls");
            printf("\n\n\n\n\n\n\t      ENTER NUMBER OF BOX YOU WANT YOUR SYMBOL IN\n\t\t\t\t SYMBOL :\n\t\t\t       PLAYER 1 : X\n\t\t\t       PLAYER 2 : O\n\t     YOU WIN BY GETTING THREE OF YOUR SYMBOL IN ROW\n\t\t      PRESS ANY KEY FOR MAIN MENUE");
            getch();
        }
        else if(c=='Q')
        {
            break;
        }
        system("cls");
    }
}
