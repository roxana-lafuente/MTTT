import re
example_string = """


<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>

<head>
    <meta http-equiv="Content-Type"
          content="text/html; charset=ISO-8859-1" />
    <title></title>
    <style type="text/css">
        table.diff {font-family:Courier; border:medium;}
        .diff_header {background-color:#e0e0e0}
        td.diff_header {text-align:right}
        .diff_next {background-color:#c0c0c0}
        .diff_add {background-color:#aaffaa}
        .diff_chg {background-color:#ffff77}
        .diff_sub {background-color:#ffaaaa}
    </style>
</head>

<body>

    <table class="diff" id="difflib_chg_to0__top"
           cellspacing="0" cellpadding="0" rules="groups" >
        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
        <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
        <tbody>
            <tr><td class="diff_next" id="difflib_chg_to0__0"><a href="#difflib_chg_to0__0">f</a></td><td class="diff_header" id="from0_1">1</td><td nowrap="nowrap">#&nbsp;TTT:&nbsp;Translators'&nbsp;Training&nbsp;Tool</td><td class="diff_next"><a href="#difflib_chg_to0__0">f</a></td><td class="diff_header" id="to0_1">1</td><td nowrap="nowrap">#&nbsp;TTT:&nbsp;Translators'&nbsp;Training&nbsp;Tool</td></tr>
            <tr><td class="diff_next" id="difflib_chg_to0__1"></td><td class="diff_header" id="from0_2">2</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_2">2</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"><a href="#difflib_chg_to0__1">n</a></td><td class="diff_header" id="from0_3">3</td><td nowrap="nowrap">##&nbsp;Mac<span class="diff_sub">hi</span>ne&nbsp;translation&nbsp;made&nbsp;easy&nbsp;for</td><td class="diff_next"><a href="#difflib_chg_to0__1">n</a></td><td class="diff_header" id="to0_3">3</td><td nowrap="nowrap">##&nbsp;Macne&nbsp;translation&nbsp;made&nbsp;easy&nbsp;for<span class="diff_add">&nbsp;human</span></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_4"></td><td nowrap="nowrap"><span class="diff_sub">human&nbsp;</span>translators!</td><td class="diff_next"></td><td class="diff_header" id="to0_4">4</td><td nowrap="nowrap">translators!</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_5">5</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_5">5</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_6">6</td><td nowrap="nowrap">TTT&nbsp;is&nbsp;an&nbsp;under&nbsp;development&nbsp;post-editing</td><td class="diff_next"></td><td class="diff_header" id="to0_6">6</td><td nowrap="nowrap">TTT&nbsp;is&nbsp;an&nbsp;under&nbsp;development&nbsp;post-editing</td></tr>
            <tr><td class="diff_next"><a href="#difflib_chg_to0__top">t</a></td><td class="diff_header" id="from0_7">7</td><td nowrap="nowrap">suite&nbsp;which&nbsp;aims&nbsp;to&nbsp;improve&nbsp;the</td><td class="diff_next"><a href="#difflib_chg_to0__top">t</a></td><td class="diff_header" id="to0_7">7</td><td nowrap="nowrap">suit<span class="diff_add">p</span>e<span class="diff_add">pee</span>&nbsp;which&nbsp;aims&nbsp;to&nbsp;improve&nbsp;the</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_8">8</td><td nowrap="nowrap">translators&nbsp;experience&nbsp;with&nbsp;machine</td><td class="diff_next"></td><td class="diff_header" id="to0_8">8</td><td nowrap="nowrap">translators&nbsp;experience&nbsp;with&nbsp;machine</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_9">9</td><td nowrap="nowrap">translation&nbsp;tools&nbsp;such&nbsp;as&nbsp;moses.&nbsp;It</td><td class="diff_next"></td><td class="diff_header" id="to0_9">9</td><td nowrap="nowrap">translation&nbsp;tools&nbsp;such&nbsp;as&nbsp;moses.&nbsp;It</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_10">10</td><td nowrap="nowrap">provides&nbsp;the&nbsp;user&nbsp;with&nbsp;a&nbsp;graphical&nbsp;user</td><td class="diff_next"></td><td class="diff_header" id="to0_10">10</td><td nowrap="nowrap">provides&nbsp;the&nbsp;user&nbsp;with&nbsp;a&nbsp;graphical&nbsp;user</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_11">11</td><td nowrap="nowrap">interface&nbsp;to:</td><td class="diff_next"></td><td class="diff_header" id="to0_11">11</td><td nowrap="nowrap">interface&nbsp;to:</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_12">12</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_12">12</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_13">13</td><td nowrap="nowrap">-&nbsp;Work&nbsp;with&nbsp;the&nbsp;moses&nbsp;machine</td><td class="diff_next"></td><td class="diff_header" id="to0_13">13</td><td nowrap="nowrap">-&nbsp;Work&nbsp;with&nbsp;the&nbsp;moses&nbsp;machine</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_14">14</td><td nowrap="nowrap">translation&nbsp;pipeline.</td><td class="diff_next"></td><td class="diff_header" id="to0_14">14</td><td nowrap="nowrap">translation&nbsp;pipeline.</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_15">15</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_15">15</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_16">16</td><td nowrap="nowrap">-&nbsp;Apply&nbsp;metrics&nbsp;such&nbsp;as&nbsp;BLEU.</td><td class="diff_next"></td><td class="diff_header" id="to0_16">16</td><td nowrap="nowrap">-&nbsp;Apply&nbsp;metrics&nbsp;such&nbsp;as&nbsp;BLEU.</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_17">17</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_17">17</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_18">18</td><td nowrap="nowrap">-&nbsp;Post-edit&nbsp;the&nbsp;obtained&nbsp;machine</td><td class="diff_next"></td><td class="diff_header" id="to0_18">18</td><td nowrap="nowrap">-&nbsp;Post-edit&nbsp;the&nbsp;obtained&nbsp;machine</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_19">19</td><td nowrap="nowrap">translation.</td><td class="diff_next"></td><td class="diff_header" id="to0_19">19</td><td nowrap="nowrap">translation.</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_20">20</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_20">20</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_21">21</td><td nowrap="nowrap">###&nbsp;Authors</td><td class="diff_next"></td><td class="diff_header" id="to0_21">21</td><td nowrap="nowrap">###&nbsp;Authors</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_22">22</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_22">22</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_23">23</td><td nowrap="nowrap">-&nbsp;Paula&nbsp;Estrella</td><td class="diff_next"></td><td class="diff_header" id="to0_23">23</td><td nowrap="nowrap">-&nbsp;Paula&nbsp;Estrella</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_24">24</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_24">24</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_25">25</td><td nowrap="nowrap">-&nbsp;Roxana&nbsp;Lafuente</td><td class="diff_next"></td><td class="diff_header" id="to0_25">25</td><td nowrap="nowrap">-&nbsp;Roxana&nbsp;Lafuente</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_26">26</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_26">26</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_27">27</td><td nowrap="nowrap">-&nbsp;Miguel&nbsp;Lemos</td><td class="diff_next"></td><td class="diff_header" id="to0_27">27</td><td nowrap="nowrap">-&nbsp;Miguel&nbsp;Lemos</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_28">28</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_28">28</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_29">29</td><td nowrap="nowrap">###&nbsp;Features</td><td class="diff_next"></td><td class="diff_header" id="to0_29">29</td><td nowrap="nowrap">###&nbsp;Features</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_30">30</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_30">30</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_31">31</td><td nowrap="nowrap">-&nbsp;Portable&nbsp;(Windows&nbsp;/&nbsp;Linux)</td><td class="diff_next"></td><td class="diff_header" id="to0_31">31</td><td nowrap="nowrap">-&nbsp;Portable&nbsp;(Windows&nbsp;/&nbsp;Linux)</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_32">32</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_32">32</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_33">33</td><td nowrap="nowrap">###&nbsp;Dependencies</td><td class="diff_next"></td><td class="diff_header" id="to0_33">33</td><td nowrap="nowrap">###&nbsp;Dependencies</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_34">34</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_34">34</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_35">35</td><td nowrap="nowrap">-&nbsp;MOSES&nbsp;(Install&nbsp;with&nbsp;"--with-mm"&nbsp;and</td><td class="diff_next"></td><td class="diff_header" id="to0_35">35</td><td nowrap="nowrap">-&nbsp;MOSES&nbsp;(Install&nbsp;with&nbsp;"--with-mm"&nbsp;and</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_36">36</td><td nowrap="nowrap">"--install-scripts"&nbsp;flags)</td><td class="diff_next"></td><td class="diff_header" id="to0_36">36</td><td nowrap="nowrap">"--install-scripts"&nbsp;flags)</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_37">37</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_37">37</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_38">38</td><td nowrap="nowrap">-&nbsp;Cygwin&nbsp;(only&nbsp;on&nbsp;Windows)</td><td class="diff_next"></td><td class="diff_header" id="to0_38">38</td><td nowrap="nowrap">-&nbsp;Cygwin&nbsp;(only&nbsp;on&nbsp;Windows)</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_39">39</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_39">39</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_40">40</td><td nowrap="nowrap">-&nbsp;GTK&nbsp;3.0</td><td class="diff_next"></td><td class="diff_header" id="to0_40">40</td><td nowrap="nowrap">-&nbsp;GTK&nbsp;3.0</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_41">41</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_41">41</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_42">42</td><td nowrap="nowrap">###&nbsp;Status</td><td class="diff_next"></td><td class="diff_header" id="to0_42">42</td><td nowrap="nowrap">###&nbsp;Status</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_43">43</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_43">43</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_44">44</td><td nowrap="nowrap">-&nbsp;Under&nbsp;development</td><td class="diff_next"></td><td class="diff_header" id="to0_44">44</td><td nowrap="nowrap">-&nbsp;Under&nbsp;development</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_45">45</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_45">45</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_46">46</td><td nowrap="nowrap">###&nbsp;How&nbsp;to&nbsp;use</td><td class="diff_next"></td><td class="diff_header" id="to0_46">46</td><td nowrap="nowrap">###&nbsp;How&nbsp;to&nbsp;use</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_47">47</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_47">47</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_48">48</td><td nowrap="nowrap">```</td><td class="diff_next"></td><td class="diff_header" id="to0_48">48</td><td nowrap="nowrap">```</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_49">49</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_49">49</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_50">50</td><td nowrap="nowrap">python&nbsp;main.py</td><td class="diff_next"></td><td class="diff_header" id="to0_50">50</td><td nowrap="nowrap">python&nbsp;main.py</td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_51">51</td><td nowrap="nowrap"></td><td class="diff_next"></td><td class="diff_header" id="to0_51">51</td><td nowrap="nowrap"></td></tr>
            <tr><td class="diff_next"></td><td class="diff_header" id="from0_52">52</td><td nowrap="nowrap">```</td><td class="diff_next"></td><td class="diff_header" id="to0_52">52</td><td nowrap="nowrap">```</td></tr>
        </tbody>
    </table>
    <table class="diff" summary="Legends">
        <tr> <th colspan="2"> Legends </th> </tr>
        <tr> <td> <table border="" summary="Colors">
                      <tr><th> Colors </th> </tr>
                      <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                      <tr><td class="diff_chg">Changed</td> </tr>
                      <tr><td class="diff_sub">Deleted</td> </tr>
                  </table></td>
             <td> <table border="" summary="Links">
                      <tr><th colspan="2"> Links </th> </tr>
                      <tr><td>(f)irst change</td> </tr>
                      <tr><td>(n)ext change</td> </tr>
                      <tr><td>(t)op</td> </tr>
                  </table></td> </tr>
    </table>
</body>

</html>

""".decode("utf-8")

final_string = example_string
pat = r'.*?\">(\d)<.*'
#pat = r'\>(?:(\d+))\<'
for m in re.finditer(pat, example_string):
    start = m.start(0) + 1
    end = m.end(0) - 1
    print (start, end)
    final_string = final_string[:start] + final_string[end:]


text_file = open("test.html", "w")
#text_file.write('\n'.join(filtered_lines))
text_file.write(final_string)
text_file.close()
#print final_string
