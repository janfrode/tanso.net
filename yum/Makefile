
all: 
	@rm -rf /var/www/html/yum/repodata
	@createrepo /var/www/html/yum
	@repoview --title "tanso.net yum repository" /var/www/html/yum

clean:
	@rm -rf /var/www/html/yum/repodata
