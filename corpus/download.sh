for i in $(seq 1 154); do
  wget -v -O $i.html "http://www.shakespeares-sonnets.com/sonnet/$i"
done
