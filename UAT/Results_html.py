def basic_info_html(adobe_passed, pagename_passed):
    html = None
    if adobe_passed and pagename_passed:
        html = '''
                <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            Adobe firing: %s<br/>
            PageName: %s<br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed is False and pagename_passed:
        html = '''
                <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            Adobe firing: %s<br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed and pagename_passed is False:
        html = '''
                <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            PageName: %s<br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed is False and pagename_passed is False:
        html = '''
                <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            Adobe firing: %s<br/>
            PageName: %s<br/>
            <b>==================</b><br/>
            '''
    return html


def localization_html(adobe_passed, pagename_passed, countrycode_passed):
    html = None

    if adobe_passed and pagename_passed and countrycode_passed:
        html = '''
            <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed is False and pagename_passed and countrycode_passed:
        html = '''
            <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            Adobe firing: %s<br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed is False and pagename_passed is False and countrycode_passed:
        html = '''
            <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            Adobe firing: %s<br/>
            PageName: %s<br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed is False and pagename_passed and countrycode_passed is False:
        html = '''
            <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            Adobe firing: %s<br/>
            Country code: %s <br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed and pagename_passed is False and countrycode_passed:
        html = '''
            <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            PageName: %s<br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed and pagename_passed is False and countrycode_passed is False:
        html = '''
            <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            Country code: %s <br/>
            PageName: %s<br/>
            <b>==================</b><br/>
            '''

    elif adobe_passed is False and pagename_passed is False and countrycode_passed is False:
        html = '''
            <b>%s</b><br/>
            <font color="%s">%s</font><br/>
            Adobe firing: %s<br/>
            Country code: %s <br/>
            PageName: %s<br/>
            <b>==================</b><br/>
            '''
    return html


def v2migration_html(adobe_passed, pagename_passed, majorVersion_passed):
    html = None

    if adobe_passed and pagename_passed and majorVersion_passed:
        html = '''
        <b>%s</b><br/>
        <font color="%s">%s</font><br/>
        <b>==================</b><br/>
        '''

    elif adobe_passed is False and pagename_passed and majorVersion_passed:
        html = '''
        <b>%s</b><br/>
        <font color="%s">%s</font><br/>
        Adobe firing: %s<br/>
        <b>==================</b><br/>
        '''

    elif adobe_passed is False and pagename_passed is False and majorVersion_passed:
        html = '''
        <b>%s</b><br/>
        <font color="%s">%s</font><br/>
        Adobe firing: %s<br/>
        PageName: %s<br/>
        <b>==================</b><br/>
        '''

    elif adobe_passed is False and pagename_passed and majorVersion_passed is False:
        html = '''
        <b>%s</b><br/>
        <font color="%s">%s</font><br/>
        Adobe firing: %s<br/>
        MajorVersion: %s<br/>
        <b>==================</b><br/>
        '''

    elif adobe_passed and pagename_passed is False and majorVersion_passed:
        html = '''
        <b>%s</b><br/>
        <font color="%s">%s</font><br/>
        PageName: %s<br/>
        <b>==================</b><br/>
        '''

    elif adobe_passed and pagename_passed is False and majorVersion_passed is False:
        html = '''
        <b>%s</b><br/>
        <font color="%s">%s</font><br/>
        MajorVersion: %s<br/>
        PageName: %s<br/>
        <b>==================</b><br/>
        '''

    elif adobe_passed is False and pagename_passed is False and majorVersion_passed is False:
        html = '''
        <b>%s</b><br/>
        <font color="%s">%s</font><br/>
        Adobe firing: %s<br/>
        MajorVersion: %s<br/>
        PageName: %s<br/>
        <b>==================</b><br/>
        '''

    return html

