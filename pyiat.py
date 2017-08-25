def iat_get_dscore_each_stim(df,subject,rt,block,condition,stimulus,cond1,cond2,blocks,weighted):
    import pandas as pd
    import numpy as np
    idx=pd.IndexSlice
    df=df[(df[condition]==cond1)|(df[condition]==cond2)]
    if weighted==True:
        blocks=sorted(blocks)
        blcnd_rt=df.groupby([subject,stimulus,condition,block])[rt].mean()
        
        #Get mean RT for each block of each condition
        cond1rt_bl1=blcnd_rt.loc[idx[:,:,cond1,[blocks[0],blocks[2]]]]
        cond1rt_bl2=blcnd_rt.loc[idx[:,:,cond1,[blocks[1],blocks[3]]]]

        cond2rt_bl1=blcnd_rt.loc[idx[:,:,cond2,[blocks[0],blocks[2]]]]
        cond2rt_bl2=blcnd_rt.loc[idx[:,:,cond2,[blocks[1],blocks[3]]]]
        
        #Drop block and condidition levels to subtract means
        cond1rt_bl1.index=cond1rt_bl1.index.droplevel([2,3])
        cond1rt_bl2.index=cond1rt_bl2.index.droplevel([2,3])
        cond2rt_bl1.index=cond2rt_bl1.index.droplevel([2,3])
        cond2rt_bl2.index=cond2rt_bl2.index.droplevel([2,3])
        
        #Get RT standard deviation separately for first and second blocks
        b1rt_std=df[(df[block]==blocks[0])|(df[block]==blocks[2])].groupby([subject,stimulus])[rt].std()
        b2rt_std=df[(df[block]==blocks[1])|(df[block]==blocks[3])].groupby([subject,stimulus])[rt].std()
        
        #Get D score
        d1=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
        d2=(cond1rt_bl2-cond2rt_bl2)/b2rt_std
        d=(d1+d2)/2
    elif weighted==False:
        cnds = df.groupby([subject,stimulus,condition])
        d = (cnds.latency.mean().unstack()[cond1]-cnds.latency.mean().unstack()[cond2])/df.groupby([subject,stimulus])[rt].std()

    return(d)



def iat_get_dscore(df,subject,rt,block,condition,cond1,cond2,blocks,weighted):
    import pandas as pd
    import numpy as np
    idx=pd.IndexSlice
    df=df[(df[condition]==cond1)|(df[condition]==cond2)]    
    if weighted==True:
        blocks=sorted(blocks)
        blcnd_rt=df.groupby([subject,condition,block])[rt].mean()
        
        #Get mean RT for each block of each condition
        cond1rt_bl1=blcnd_rt.loc[idx[:,cond1,[blocks[0],blocks[2]]]]
        cond1rt_bl2=blcnd_rt.loc[idx[:,cond1,[blocks[1],blocks[3]]]]

        cond2rt_bl1=blcnd_rt.loc[idx[:,cond2,[blocks[0],blocks[2]]]]
        cond2rt_bl2=blcnd_rt.loc[idx[:,cond2,[blocks[1],blocks[3]]]]
        
        #Drop block and condidition levels to subtract means
        for df_tmp in [cond1rt_bl1,cond1rt_bl2,cond2rt_bl1,cond2rt_bl2]:
            df_tmp.index=df_tmp.index.droplevel([1,2])
        
        #Get RT standard deviation separately for first and second blocks
        b1rt_std=df[(df[block]==blocks[0])|(df[block]==blocks[2])].groupby(subject)[rt].std()
        b2rt_std=df[(df[block]==blocks[1])|(df[block]==blocks[3])].groupby(subject)[rt].std()
        
        #Get D score
        d1=(cond1rt_bl1-cond2rt_bl1)/b1rt_std
        d2=(cond1rt_bl2-cond2rt_bl2)/b2rt_std
        d=(d1+d2)/2
        d=pd.concat([d1,d2,d],axis=1)
        d.columns=['dscore1','dscore2','dscore']
        return(d)
    elif weighted==False:
        cnds = df.groupby([subject,condition])
        d = (cnds.latency.mean().unstack()[cond1]-cnds.latency.mean().unstack()[cond2])/df.groupby(subject)[rt].std()
        d.name='dscore'
        return(d)

def blcnd_extract(df,var,subject,condition,block,cond1,cond2,blocks,flag_outformat='pct',include_blocks=True):
    import pandas as pd
    import numpy as np
    idx=pd.IndexSlice
    if flag_outformat=='pct':
        all_df=df.groupby(subject)[var].mean()
        ##By condition
        cond1_df=df[(df[condition]==cond1)].groupby(subject)[var].mean()
        cond2_df=df[(df[condition]==cond2)].groupby(subject)[var].mean()
        ##By condition and block
        if include_blocks == True:
            blcnd=df.groupby([subject,condition,block])[var].mean()
    elif flag_outformat=='sum':
        all_df=df.groupby(subject)[var].sum()
        ##By condition
        cond1_df=df[(df[condition]==cond1)].groupby(subject)[var].sum()
        cond2_df=df[(df[condition]==cond2)].groupby(subject)[var].sum()
        ##By condition and block
        if include_blocks == True:
            blcnd=df.groupby([subject,condition,block])[var].sum()
    elif flag_outformat=='count':
        all_df=df.groupby(subject)[var].count()
        ##By condition
        cond1_df=df[(df[condition]==cond1)].groupby(subject)[var].count()
        cond2_df=df[(df[condition]==cond2)].groupby(subject)[var].count()
        ##By condition and block
        if include_blocks == True:
            blcnd=df.groupby([subject,condition,block])[var].count()
    if include_blocks == True:
        cond1_bl1=blcnd.loc[idx[:,cond1,[blocks[0],blocks[2]]]]
        cond1_bl2=blcnd.loc[idx[:,cond1,[blocks[1],blocks[3]]]]
        cond2_bl1=blcnd.loc[idx[:,cond2,[blocks[0],blocks[2]]]]
        cond2_bl2=blcnd.loc[idx[:,cond2,[blocks[1],blocks[3]]]]
        #Drop block and condidition levels to subtract means
        for df_tmp in [cond1_bl1,cond1_bl2,cond2_bl1,cond2_bl2]:
            df_tmp.index=df_tmp.index.droplevel([1,2])
        out=pd.concat([all_df,cond1_df,cond2_df,cond1_bl1,cond1_bl2,cond2_bl1,cond2_bl2],axis=1)
    elif include_blocks == False:
        out=pd.concat([all_df,cond1_df,cond2_df],axis=1)
    return(out)

def analyze_iat(df,subject,rt,correct,condition,cond1,cond2,block,blocks=[2,3,5,6],weighted=True,\
        fast_rt=400,slow_rt=10000,\
        overall_err_cut=.3,cond_err_cut=.4,block_err_cut=.4,\
        overall_fastslowRT_cut=.10,cond_fastslowRT_cut=.25,block_fastslowRT_cut=.25,\
        num_blocks_cutoff=4,\
        fastslow_stats=False,error_or_correct='correct',errors_after_fastslow_rmvd=False,flag_outformat='pct',print_to_excel=False,\
        each_stim=False,stimulus=False):

    """Takes a dataframe containing raw IAT data (all trials, all subjects) and returns
         the number of blocks, percentage of errors, reaction times that are too fast and too slow, 
         flags to remove subjects and D scores for each subject.

     Parameters
     ----------
     df : pandas dataframe 
         Containing raw IAT data
     subject : str
         Column name containing subject number
     rt : str
         Column name containing reaction time (in ms) for each trial
     correct : str
         Column name containing whether trial was correct (where correct = 1, error = 0)
         (can also use if columns specifies errors; see 'error_or_correct' parameter)
     condition : str
         Column name containing condition (e.g. Black-Good\White-Bad vs. Black-Bad\White-Good)
     cond1 : str
         Name of first of two conditions (e.g. 'Black-Good\White-Bad'): bias for this condition will result in positive D score  
     cond2 : str
         Name of second of two conditions (e.g. 'Black-Bad\White-Good'): bias for this condition will result in negative D score
     block : str
         Column that contains block information
     blocks : list
         A list containing the numbers corresponding to the relevant blocks, default : [2,3,5,6]
     weighted : Boolean
         If True return weighted D scores; if False return unweighted D scores, default : True
     fast_rt : int
         Reaction time (in ms) that is too fast, default: 400
     slow_rt : int
         Reaction time (in ms) that is too slow, default: 10000
     overall_err_cut : float
         Cutoff for subject exclusion: overall error rate (decimal), default : .3
     cond_err_cut : float
         Cutoff for subject exclusion: error rate (decimal) within each condition, default : .4
     block_err_cut : float
         Cutoff for subject exclusion: error rate (decimal) within a single block, default : .4
     overall_fastslowRT_cut=.10
         Cutoff for subject exclusion: overall rate of trials with too fast or too slow RT (decimal), default : .1
     cond_fastslowRT_cut : float
         Cutoff for subject exclusion: rate of trials with too fast or too slow RT (decimal) within each condition, default : .25
     block_fastslowRT_cut : float
         Cutoff for subject exclusion: rate of trials with too fast or too slow RT (decimal) within each block, default : .25
     num_blocks_cutoff : int
         Cutoff for subject exclusion: Number of blocks required, default : 4
     error_or_correct : str
         Enter 'error' to enter a column for 'correct' where error = 1, correct = 0, default: 'correct'
     errors_after_fastslow_rmvd : Boolean
            If True calculates error rates after removing all fast\slow trials (similar to R package iat); if False error rates calculated with all trials, default : False
     fastslow_stats : Boolean
         Return a second dataframe containing the number and percentage of fast\slow trials across all subjects
         and across subjects with usable data, default : False
     flag_outformat : str
         Can enter 'count' to return number of errors and too fast\slow trials (if fastslow_stats set to True), default : 'pct'
     print_to_excel : Boolean
         Print an excel workbook that contains output, default : False
     each_stim : Boolean
         Return D scores for each individual stimulus (i.e. word), default : False
     stimulus
         If each stim = True, then give name of column containing each stimulus (i.e. word), default : False

     Returns
     -------
     pandas DataFrame with 
        -error rates (overall, each condition, each block (error rates *include* fast\slow trials)),
        -rates of fast\slow trials (overall, each condition, each block)
        -exclusion flags (overall flag indicating subject should be excluded and for each category informing why subject was flagged)
        -D scores (overall and block 1 and block 2 if weighted)
    if fastslow_stats = True:
        pandas DataFrame with rates of fast\slow trials across all subjects and across only subjects NOT flagged for exclusion
        (to report the overall number\pct of trials excluded from a study)

     Examples
     --------
     >>> weighted_d,fastslow_stats_df=iat(it,subject='session_id',rt='latency',
     ...                 condition='cond',correct='correct',
     ...                 cond1='nosh_me',cond2='sh_me',block='block',
     ...                 blocks=[2,3,5,6],fastslow_stats=True,each_stim=False,
     ...                 stimulus='trial_name')
    
    
     """
    import pandas as pd
    from pandas import ExcelWriter
    import numpy as np
    idx=pd.IndexSlice
    df=df[(df[condition]==cond1)|(df[condition]==cond2)] 

    if weighted == True:

        #All column names for output
        col_names=['overall_error_rate','%s_error_rate'%cond1,'%s_error_rate'%cond2,\
        '%s_bl1_error_rate'%cond1,'%s_bl2_error_rate'%cond1,'%s_bl1_error_rate'%cond2,'%s_bl2_error_rate'%cond2,\

        'overall_fast_rt_rate_%dms'%(fast_rt),\
        '%s_fast_rt_rate_%dms'%(cond1,fast_rt),'%s_fast_rt_rate_%dms'%(cond2,fast_rt),\
        '%s_bl1_fast_rt_rate_%dms'%(cond1,fast_rt),'%s_bl2_fast_rt_rate_%dms'%(cond1,fast_rt),\
        '%s_bl1_fast_rt_rate_%dms'%(cond2,fast_rt),'%s_bl2_fast_rt_rate_%dms'%(cond2,fast_rt),\

        'overall_slow_rt_rate_%dms'%(slow_rt),\
        '%s_slow_rt_rate_%dms'%(cond1,slow_rt),'%s_slow_rt_rate_%dms'%(cond2,slow_rt),\
        '%s_bl1_slow_rt_rate_%dms'%(cond1,slow_rt),'%s_bl2_slow_rt_rate_%dms'%(cond1,slow_rt),\
        '%s_bl1_slow_rt_rate_%dms'%(cond2,slow_rt),'%s_bl2_slow_rt_rate_%dms'%(cond2,slow_rt),\
        'num_blocks']
        
        #Column names for 1\0 output regarding which criteria were flagged (errors, too many fast or slow trials)
        flag_col_names= ['%s_flag'%i for i in col_names]

        #Column names for number of trials overall, within condition and within block 
        #(with a switch to name both before and after excluding fast\slow trials)
        incl_excl_switch='incl'
        block_num_col_names=['overall_num_trls_%s_fastslow_rt'%(incl_excl_switch),\
        '%s_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),'%s_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch),\
        '%s_bl1_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),'%s_bl2_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),\
        '%s_bl1_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch),'%s_bl2_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch)]

        
        ##Cutoffs for the pct of errors or fast or slow trials that's considered excessive
        cutoffs=[overall_err_cut,cond_err_cut,cond_err_cut,\
                 block_err_cut,block_err_cut,\
                 block_err_cut,block_err_cut,\
                 overall_fastslowRT_cut,cond_fastslowRT_cut,cond_fastslowRT_cut,\
                 block_fastslowRT_cut,block_fastslowRT_cut,\
                 block_fastslowRT_cut,block_fastslowRT_cut,\
                 overall_fastslowRT_cut,cond_fastslowRT_cut,cond_fastslowRT_cut,\
                 block_fastslowRT_cut,block_fastslowRT_cut,\
                 block_fastslowRT_cut,block_fastslowRT_cut,num_blocks_cutoff]

        ## Number of blocks for each subject
        num_blocks=df.groupby([subject])[block].unique().apply(lambda x: len(x))

        ##########################################################################################
        #Get overall pct of errors, fast trials, slow trials as well as pct per condition and per block
        ##########################################################################################
        
        #Remove trials that are too fast or too slow
        df_fastslow_rts_rmvd=df[-(df[rt]>=slow_rt)]
        df_fastslow_rts_rmvd=df_fastslow_rts_rmvd[-(df_fastslow_rts_rmvd[rt]<fast_rt)]

        ##Errors
        if errors_after_fastslow_rmvd == False:
            df_err=df
        elif errors_after_fastslow_rmvd == True:
            df_err=df_fastslow_rts_rmvd
        ###Can enter either column where errors are 1 and correct responses are 0 or vice versa
        if error_or_correct=='error':
            err_vars=blcnd_extract(df_err,correct,subject,condition,block,cond1,cond2,blocks,flag_outformat)
        elif error_or_correct=='correct':
            err_vars=1-blcnd_extract(df_err,correct,subject,condition,block,cond1,cond2,blocks,flag_outformat)

        #Fast RT
        df['fast_rt']=(df[rt]<fast_rt)*1
        fast_rt_vars=blcnd_extract(df,'fast_rt',subject,condition,block,cond1,cond2,blocks,flag_outformat)

        #Slow RT
        df['slow_rt']=(df[rt]>=slow_rt)*1
        slow_rt_vars=blcnd_extract(df,'slow_rt',subject,condition,block,cond1,cond2,blocks,flag_outformat)


        outcms=[err_vars,\
                fast_rt_vars,\
                slow_rt_vars,\
                num_blocks]

        #Put together and put into rates - containing just the rates - 
        #and flags (i.e. whether the rate ) is over a threshold
        flags=pd.DataFrame(columns=flag_col_names,index=df[subject].unique())
        rates=pd.concat(outcms,axis=1)
        rates.columns=col_names

        for col,fcol,cutoff in zip(col_names,flag_col_names,cutoffs):
            if col!='num_blocks':
                flags.loc[:,fcol]=((rates[col]>cutoff)*1)
            elif col=='num_blocks':
                flags.loc[:,fcol]=((rates[col]<cutoff)*1)

        flags['iat_flag']=flags.sum(axis=1)       

        #Figure out number of trials in each block and total number of fast and slow trials (and remove them)

        pre_trl_count_vars=blcnd_extract(df,rt,subject,condition,block,cond1,cond2,blocks,flag_outformat='count')
        pre_trl_count_vars.columns=block_num_col_names

        #Count and remove with all fast and slow trials and recount num of trials
        all_fast_rt_count_all_subs=df[df[rt]<fast_rt][rt].count()
        all_slow_rt_count_all_subs=df[df[rt]>=slow_rt][rt].count()
        all_fast_rt_pct_all_subs=df[df[rt]<fast_rt][rt].count()/df[rt].count().astype(float)
        all_slow_rt_pct_all_subs=df[df[rt]>=slow_rt][rt].count()/df[rt].count().astype(float)

        #Figure out number of trials after removing fast\slow rt trials 
        #in each block and total number of fast and slow trials (and remove them)
        post_trl_count_vars=blcnd_extract(df_fastslow_rts_rmvd,rt,subject,condition,block,cond1,cond2,blocks,flag_outformat='count')
        incl_excl_switch='excl'
        block_num_col_names=['overall_num_trls_%s_fastslow_rt'%(incl_excl_switch),\
        '%s_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),'%s_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch),\
        '%s_bl1_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),'%s_bl2_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),\
        '%s_bl1_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch),'%s_bl2_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch)]
        post_trl_count_vars.columns=block_num_col_names
        
        ###############################################################################################################################
        ###############################################################################################################################
    #Only return overall and condition requirements but not block
    elif weighted == False:

        #All column names for output
        col_names=['overall_error_rate','%s_error_rate'%cond1,'%s_error_rate'%cond2,\
        
        'overall_fast_rt_rate_%dms'%(fast_rt),\
        '%s_fast_rt_rate_%dms'%(cond1,fast_rt),'%s_fast_rt_rate_%dms'%(cond2,fast_rt),\
    
        'overall_slow_rt_rate_%dms'%(slow_rt),\
        '%s_slow_rt_rate_%dms'%(cond1,slow_rt),'%s_slow_rt_rate_%dms'%(cond2,slow_rt)]
        
        #Column names for 1\0 output regarding which criteria were flagged (errors, too many fast or slow trials)
        flag_col_names= ['%s_flag'%i for i in col_names]

        #Column names for number of trials overall, within condition and within block 
        #(with a switch to name both before and after excluding fast\slow trials)
        incl_excl_switch='incl'
        block_num_col_names=['overall_num_trls_%s_fastslow_rt'%(incl_excl_switch),\
        '%s_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),'%s_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch)]
        
        ##Cutoffs for the pct of errors or fast or slow trials that's considered excessive
        cutoffs=[overall_err_cut,cond_err_cut,cond_err_cut,\
                 overall_fastslowRT_cut,cond_fastslowRT_cut,cond_fastslowRT_cut,\
                 overall_fastslowRT_cut,cond_fastslowRT_cut,cond_fastslowRT_cut]

        ##########################################################################################
        #Get overall pct of errors, fast trials, slow trials as well as pct per condition and per block
        ##########################################################################################
        
        #Remove trials that are too fast or too slow
        df_fastslow_rts_rmvd=df[-(df[rt]>=slow_rt)]
        df_fastslow_rts_rmvd=df_fastslow_rts_rmvd[-(df_fastslow_rts_rmvd[rt]<fast_rt)]

        ##Errors
        if errors_after_fastslow_rmvd == False:
            df_err=df
        elif errors_after_fastslow_rmvd == True:
            df_err=df_fastslow_rts_rmvd
        
        ###Can enter either column where errors are 1 and correct responses are 0 or vice versa
        if error_or_correct=='error':
            err_vars=blcnd_extract(df_err,errs,subject,condition,block,cond1,cond2,blocks,flag_outformat,include_blocks=False)
        elif error_or_correct=='correct':
            err_vars=1-blcnd_extract(df_err,correct,subject,condition,block,cond1,cond2,blocks,flag_outformat,include_blocks=False)

        #Fast RT
        df['fast_rt']=(df[rt]<fast_rt)*1
        fast_rt_vars=blcnd_extract(df,'fast_rt',subject,condition,block,cond1,cond2,blocks,flag_outformat,include_blocks=False)

        #Slow RT
        df['slow_rt']=(df[rt]>=slow_rt)*1
        slow_rt_vars=blcnd_extract(df,'slow_rt',subject,condition,block,cond1,cond2,blocks,flag_outformat,include_blocks=False)


        outcms=[err_vars,\
                fast_rt_vars,\
                slow_rt_vars]

        #Put together and put into rates - containing just the rates - 
        #and flags (i.e. whether the rate ) is over a threshold
        flags=pd.DataFrame(columns=flag_col_names,index=df[subject].unique())
        rates=pd.concat(outcms,axis=1)
        rates.columns=col_names

        for col,fcol,cutoff in zip(col_names,flag_col_names,cutoffs):
            flags.loc[:,fcol]=((rates[col]>cutoff)*1)

        flags['iat_flag']=flags.sum(axis=1)       

        #Figure out number of trials in each block and total number of fast and slow trials (and remove them)

        pre_trl_count_vars=blcnd_extract(df,rt,subject,condition,block,cond1,cond2,blocks,include_blocks=False,flag_outformat='count')
        pre_trl_count_vars.columns=block_num_col_names

        #Count and remove with all fast and slow trials and recount num of trials
        all_fast_rt_count_all_subs=df[df[rt]<fast_rt][rt].count()
        all_slow_rt_count_all_subs=df[df[rt]>=slow_rt][rt].count()
        all_fast_rt_pct_all_subs=df[df[rt]<fast_rt][rt].count()/df[rt].count().astype(float)
        all_slow_rt_pct_all_subs=df[df[rt]>=slow_rt][rt].count()/df[rt].count().astype(float)

        #Remove trials that are too fast or too slow
        df_fastslow_rts_rmvd=df[-(df[rt]>=slow_rt)]
        df_fastslow_rts_rmvd=df_fastslow_rts_rmvd[-(df_fastslow_rts_rmvd[rt]<fast_rt)]

        #Figure out number of trials after removing fast\slow rt trials 
        #in each block and total number of fast and slow trials (and remove them)
        post_trl_count_vars=blcnd_extract(df_fastslow_rts_rmvd,rt,subject,condition,block,cond1,cond2,blocks,include_blocks=False,flag_outformat='count')
        incl_excl_switch='excl'
        block_num_col_names=['overall_num_trls_%s_fastslow_rt'%(incl_excl_switch),\
        '%s_num_trls_%s_fastslow_rt'%(cond1,incl_excl_switch),'%s_num_trls_%s_fastslow_rt'%(cond2,incl_excl_switch)]
        post_trl_count_vars.columns=block_num_col_names

    all_num_trl_per_block=pd.concat([pre_trl_count_vars,post_trl_count_vars],axis=1)
    #Get D scores
    if each_stim==False:
        d=iat_get_dscore(df_fastslow_rts_rmvd,subject,rt,block,condition,cond1,cond2,blocks,weighted)
        if weighted == False:
            d=d.to_frame()
    elif each_stim==True:
        d=iat_get_dscore_each_stim(df_fastslow_rts_rmvd,subject,rt,block,condition,stimulus,cond1,cond2,blocks,weighted)
        d=d.unstack()
    
    all_iat_out = pd.concat([all_num_trl_per_block,rates,flags,d],axis=1)

    #Print output to excel
    if print_to_excel==True:

        from datetime import datetime
        dt=datetime.now()
        dt=dt.strftime('%m_%d_%Y_%H_%M_%S')

        iat_excel = ExcelWriter('pyiat_output_%s.xlsx'%dt)
        all_iat_out.to_excel('pyiat_output_%s.xlsx'%dt,sheet_name='pyiat')
        

    if fastslow_stats == True:
        #Count and remove with all fast and slow trials and recount num of trials
        df_no_flag=df[df[subject].isin(flags[flags.iat_flag==0].index)].copy(deep=True)
        
        all_fast_rt_count_incl_subs=df_no_flag[(df_no_flag[rt]<fast_rt)][rt].count()
        all_slow_rt_count_incl_subs=df_no_flag[(df_no_flag[rt]>=slow_rt)][rt].count()
        all_fast_rt_pct_incl_subs=df_no_flag[(df_no_flag[rt]<fast_rt)][rt].count()/df_no_flag[rt].count().astype(float)
        all_slow_rt_pct_incl_subs=df_no_flag[(df_no_flag[rt]>=slow_rt)][rt].count()/df_no_flag[rt].count().astype(float)


        all_fast_slow_rt=pd.DataFrame([all_fast_rt_count_all_subs,all_fast_rt_pct_all_subs,\
                                       all_slow_rt_count_all_subs,all_slow_rt_pct_all_subs,\
                                       all_fast_rt_count_incl_subs,all_fast_rt_pct_incl_subs,\
                                       all_slow_rt_count_incl_subs,all_slow_rt_pct_incl_subs],
                                       index=['fast_rt_count_all_subs','fast_rt_pct_all_subs',\
                                              'slow_rt_count_all_subs','slow_rt_pct_all_subs',\
                                              'fast_rt_count_included_subs','fast_rt_pct_included_subs',\
                                              'slow_rt_count_included_subs','slow_rt_pct_included_subs']\
                                              ,columns=['fast_slow_rt'])
        if print_to_excel==True:
            all_fast_slow_rt.to_excel('pyiat_output_%s.xlsx'%dt,sheet_name='Num_Pct_Fast_Slow_RT_Trials')
            iat_excel.save()
        return(all_iat_out,all_fast_slow_rt)
    elif fastslow_stats == False:
        if print_to_excel==True:
            iat_excel.save()
        return(all_iat_out)
        #return(d,rates,flags,all_num_trl_per_block,all_fast_slow_rt)
        #rates,flags,all_num_trl_per_block,all_fast_slow_rt