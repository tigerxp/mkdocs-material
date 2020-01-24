import re

from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import Text, Name, Number, String, Comment, Punctuation, \
     Other, Keyword, Operator, Literal, Whitespace

class AdsiLexer(RegexLexer):
    """
    For ADSI code.

    """
    name = 'Adsi'
    aliases = ['adsi', 'ADSI']
    filenames = ['*.adsi']
    mimetypes = ['text/x-powershell']

    flags = re.DOTALL | re.IGNORECASE | re.MULTILINE

    keywords = (
        'while validateset validaterange validatepattern validatelength '
        'validatecount until trap switch return ref process param parameter in '
        'if global: function foreach for finally filter end elseif else '
        'dynamicparam do default continue cmdletbinding break begin alias \\? '
        '% #script #private #local #global mandatory parametersetname position '
        'valuefrompipeline valuefrompipelinebypropertyname '
        'valuefromremainingarguments helpmessage try catch throw').split()

    operators = (
        'and as band bnot bor bxor casesensitive ccontains ceq cge cgt cle '
        'clike clt cmatch cne cnotcontains cnotlike cnotmatch contains '
        'creplace eq exact f file ge gt icontains ieq ige igt ile ilike ilt '
        'imatch ine inotcontains inotlike inotmatch ireplace is isnot le like '
        'lt match ne not notcontains notlike notmatch or regex replace '
        'wildcard').split()

    verbs = (
        'write where watch wait use update unregister unpublish unprotect '
        'unlock uninstall undo unblock trace test tee take sync switch '
        'suspend submit stop step start split sort skip show set send select '
        'search scroll save revoke resume restore restart resolve resize '
        'reset request repair rename remove register redo receive read push '
        'publish protect pop ping out optimize open new move mount merge '
        'measure lock limit join invoke install initialize import hide group '
        'grant get format foreach find export expand exit enter enable edit '
        'dismount disconnect disable deny debug cxnew copy convertto '
        'convertfrom convert connect confirm compress complete compare close '
        'clear checkpoint block backup assert approve aggregate add').split()

    aliases_ = (
        'ac asnp cat cd cfs chdir clc clear clhy cli clp cls clv cnsn '
        'compare copy cp cpi cpp curl cvpa dbp del diff dir dnsn ebp echo epal '
        'epcsv epsn erase etsn exsn fc fhx fl foreach ft fw gal gbp gc gci gcm '
        'gcs gdr ghy gi gjb gl gm gmo gp gps gpv group gsn gsnp gsv gu gv gwmi '
        'h history icm iex ihy ii ipal ipcsv ipmo ipsn irm ise iwmi iwr kill lp '
        'ls man md measure mi mount move mp mv nal ndr ni nmo npssc nsn nv ogv '
        'oh popd ps pushd pwd r rbp rcjb rcsn rd rdr ren ri rjb rm rmdir rmo '
        'rni rnp rp rsn rsnp rujb rv rvpa rwmi sajb sal saps sasv sbp sc select '
        'set shcm si sl sleep sls sort sp spjb spps spsv start sujb sv swmi tee '
        'trcm type wget where wjb write').split()

    commenthelp = (
        'component description example externalhelp forwardhelpcategory '
        'forwardhelptargetname functionality inputs link '
        'notes outputs parameter remotehelprunspace role synopsis').split()

    tokens = {
        'root': [
            # we need to count pairs of parentheses for correct highlight
            # of '$(...)' blocks in strings
            (r'\(', Punctuation, 'child'),
            (r'\s+', Text),
            (r'^(\s*#[#\s]*)(\.(?:%s))([^\n]*$)' % '|'.join(commenthelp),
             bygroups(Comment, String.Doc, Comment)),
            (r'#[^\n]*?$', Comment),
            (r'(&lt;|<)#', Comment.Multiline, 'multline'),
            (r'@"\n', String.Heredoc, 'heredoc-double'),
            (r"@'\n.*?\n'@", String.Heredoc),
            # escaped syntax
            (r'`[\'"$@-]', Punctuation),
            (r'"', String.Double, 'string'),
            (r"'([^']|'')*'", String.Single),
            (r'(\$|@@|@)((global|script|private|env):)?\w+',
             Name.Variable),
            (r'(%s)\b' % '|'.join(keywords), Keyword),
            (r'-(%s)\b' % '|'.join(operators), Operator),
            (r'(%s)-[a-z_]\w*\b' % '|'.join(verbs), Name.Builtin),
            (r'(%s)\s' % '|'.join(aliases_), Name.Builtin),
            (r'\[[a-z_\[][\w. `,\[\]]*\]', Name.Constant),  # .net [type]s
            (r'-[a-z_]\w*', Name),
            (r'\w+', Name),
            (r'[.,;@{}\[\]$()=+*/\\&%!~?^`|<>-]|::', Punctuation),
        ],
        'child': [
            (r'\)', Punctuation, '#pop'),
            include('root'),
        ],
        'multline': [
            (r'[^#&.]+', Comment.Multiline),
            (r'#(>|&gt;)', Comment.Multiline, '#pop'),
            (r'\.(%s)' % '|'.join(commenthelp), String.Doc),
            (r'[#&.]', Comment.Multiline),
        ],
        'string': [
            (r"`[0abfnrtv'\"$`]", String.Escape),
            (r'[^$`"]+', String.Double),
            (r'\$\(', Punctuation, 'child'),
            (r'""', String.Double),
            (r'[`$]', String.Double),
            (r'"', String.Double, '#pop'),
        ],
        'heredoc-double': [
            (r'\n"@', String.Heredoc, '#pop'),
            (r'\$\(', Punctuation, 'child'),
            (r'[^@\n]+"]', String.Heredoc),
            (r".", String.Heredoc),
        ]
    }
