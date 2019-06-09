paper.pdf: paper.md
	pandoc $< -o $@ --template=template.tex

all: paper.pdf

clean:
	rm -f paper.pdf

.PHONY: all clean
