#!bin/bash
for f in *.txt; do # cycle through all *.txt files
  if [ ! -f "${f%.*}.gif" ]; then # https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
      # if there is not a gif of the same name, create temp folder
      mkdir temp
      cp "$f" "temp/$f"
      cd temp
      # generate images into the temp folder using python program
      python3 ../game_sequence.py "${f%.*}" # https://www.tutorialspoint.com/python/python_command_line_arguments.htm
      # join images into gif
      convert -delay 40 -loop 0 *.png "${f%.*}.gif" # https://askubuntu.com/questions/648244/how-do-i-create-an-animated-gif-from-still-images-preferably-with-the-command-l
      cp "${f%.*}.gif" "../${f%.*}.gif"
      # remove temp folder
      cd ..
      rm -r temp
  fi
done
