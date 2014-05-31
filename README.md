# Connect Subversion to Trac

It can record every commit into *sqlite* files, you can get summary of every commit actions and text lines from the database.
  
  
# Requirement

* Trac 
* Subversion

  
# Usage 

Put this lines into your pre-commit file, and make it executable:

    python [path to this code]/pre_commit_tmpl.py $1 $2

And then the post-commit file like this:

    python [path to this code]/post_commit_tmpl.py $1 $2


And then, all commit log should start with '[ticket:xxx]', the ticket could be a piece of requirement , or a bug etc.
  
  
   