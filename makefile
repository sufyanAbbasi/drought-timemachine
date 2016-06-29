NAME=drought
EXPORT_DIR = ./exported-tiles-${NAME}/
TMC=./${NAME}-timemachine.tmc
TIMEMACHINE=./${NAME}_Timelapse.timemachine
all:
	rm -rf $(TIMEMACHINE)
	rm -rf $(TMC) 
	python processMapTiles.py -s $(EXPORT_DIR) -d $(TMC)
	ruby ~/../../Applications/Time\ Machine\ Creator.app/Contents/ct/ct.rb $(TMC) $(TIMEMACHINE)	
tiles:
	rm -rf $(TMC)
	python processMapTiles.py -s $(EXPORT_DIR) -d $(TMC)

timemachine:
	rm -rf $(TIMEMACHINE)
	ruby ~/../../Applications/Time\ Machine\ Creator.app/Contents/ct/ct.rb $(TMC) $(TIMEMACHINE)

clean:
	rm -rf $(TMC)
	rm -rf $(TIMEMACHINE)
