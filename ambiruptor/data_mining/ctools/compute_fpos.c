#include "stdio.h"
#include "string.h"

#define MAXI 1<<20
char buffer[MAXI];

int main(int argc, char **argv)
{
  if (argc != 3)
  {
    puts("Wrong number of arguments (2 expected)");
    return 1;
  }
  
  FILE *in = fopen(argv[1], "rb");
  if (in == NULL)
  {
    puts("Can't open input file.");
    return 1;
  }
  
  FILE *out = fopen(argv[2], "wb");
  if (out == NULL)
  {
    puts("Can't open output file.");
    return 1;
  }
  
  char tag_title_str[] = "<title>";
  char tag_text_str[]  = "<text xml:space=\"preserve\">";
  int  tag_title_size = strlen(tag_title_str);
  int  tag_text_size  = strlen(tag_text_str);
  int  tag_title_pos = 0;
  int  tag_text_pos  = 0;
  
  enum mode { NONE, TITLE, TEXT };
  enum mode current_mode = NONE;
  
  size_t position_act = 0;
  size_t position_last = 0;
  
  size_t buffer_size = 0;
  size_t buffer_pos = 0;
  while (1)
  {
    if (buffer_pos >= buffer_size)
    {
      buffer_pos = 0;
      buffer_size = fread(buffer, sizeof(char), MAXI, in);
    }
    if (buffer_size == 0)
      break;
    char c = buffer[buffer_pos++];
    
    if (c == tag_title_str[tag_title_pos])
    {
      if (++tag_title_pos == tag_title_size)
      {
        current_mode = TITLE;
        position_last = position_act+1;
      }
    }
    else
    {
      tag_title_pos = 0;
    }
    
    if (c == tag_text_str[tag_text_pos])
    {
      if (++tag_text_pos == tag_text_size)
      {
        current_mode = TEXT;
        position_last = position_act+1;
      }
    }
    else
    {
      tag_text_pos = 0;
    }
    
    if (c == '<')
    {
      if (current_mode != NONE)
      {
        fwrite(&position_last, sizeof(size_t), 1, out);
        size_t s = position_act - position_last;
        fwrite(&s, sizeof(size_t), 1, out);
      }
    }
    
    position_act++;
  }
  
  fclose(in);
  fclose(out);
}
