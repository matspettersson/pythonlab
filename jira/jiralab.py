from jira import JIRA
import locale, pprint
from configparser import ConfigParser

#https://jira.readthedocs.io/en/master/examples.html#id10


locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')

CONFIG_FILE = "jira.conf"

parser = ConfigParser()
parser.read(CONFIG_FILE)

user = parser.get('jira','user')
apikey = parser.get('jira','apikey')
server = parser.get('jira','server')

options = {
 'server': server
}

jira = JIRA(options, basic_auth=(user,apikey) )


# Show all the projects
def showProjects():
   print("Showing all projects")

   for project in jira.projects():
# to dump all the properties
#     itemDir = project.__dict__
#     for i in itemDir:
#        print('{0}  :  {1}'.format(i, itemDir[i]))

     print("Project: {} - {}".format(project.key, project.name)) 
   return


# Show all the epics (that are not done), order by duedate
def showEpics(project):
   print("Showing epics for project: {}".format(project))
   issues = jira.search_issues('project={} and status != Done and type = Epic order by duedate'.format(project))
   for issue in issues:
     print('Issue Key:{}, Summary:{}, Type name:{}, Status:{}'.format(issue.key, issue.fields.summary, issue.fields.issuetype.name, issue.fields.status.name))
   return


# Search returns first 50 results, `maxResults` must be set to exceed this
def showOpenIssues(project):

   issues_in_proj = jira.search_issues("project={} and status != Done".format(project))
#print(issues_in_proj)
   for issue in issues_in_proj:
      print('Issue Key:{}, Summary:{}, Type name:{}, Status:{}'.format(issue.key, issue.fields.summary, issue.fields.issuetype.name, issue.fields.status.name))
   return


# Show my open issues
def myOpenIssues():
   print("Showing my open issues")
   issues = jira.search_issues('assignee = currentUser() and status != Done order by duedate')
   for issue in issues:
     print('Issue Key:{}, Summary:{}, Type name:{}, Status:{}'.format(issue.key, issue.fields.summary, issue.fields.issuetype.name, issue.fields.status.name))
   return


# Show my open issues due by the end of the week
def myOpenIssuesDueThisWeek():
   print("Showing my open issues due by the end of the week")
   issues = jira.search_issues('assignee = currentUser() and due < endOfWeek() order by priority desc')
   for issue in issues:
     print('Issue Key:{}, Summary:{}, Type name:{}, Status:{}'.format(issue.key, issue.fields.summary, issue.fields.issuetype.name, issue.fields.status.name))
   return

#print([issue.fields.summary, issue.fields.description, issue.fields.project, issue.fields.issuetype,issue.fields.id for issue in #issues])



def main():
   showProjects()
#    showEpics("MAS")
#    showOpenIssues("MAS")
   myOpenIssues()
#   myOpenIssuesDueThisWeek()
   return

if __name__== "__main__":
  main()
