#TEXTFILES := $(wildcard *.txt)
#BASENAMES := $(basename $(TEXTFILES))
#HTMLFILES := $(addsuffix .html, $(BASENAMES))
#all: $(HTMLFILES)
#asciidoc -a badges -a icons --conf-file=/var/www/html/layout.conf $<

OBJECTS = $(patsubst %.txt,%.html,$(wildcard *.txt))

all: $(OBJECTS)

%.html: %.txt
	asciidoc --conf-file=/var/www/html/layout.conf $<

clean:
	rm -f $(OBJECTS)
