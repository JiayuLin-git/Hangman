import json as js
import re
import requests
import sys
class DictManager:
    #predict letter probability
    def __init__(self):
        pass
    # deal the current dictionary
    # input currentdic: current guessing dictionary package receive from webservice
    # input type:dictionary
    # return wordlist: words need guessing that split into list
    # rtype: list
    def cleandic(self,currentdic):
        wordlist=re.split(r'\W+', currentdic['state'])
        wordlist.remove('')
        return wordlist
    # get length of every current guessing word
    # input currentdic:current guessing dictionary package receive from webservice
    # input type: dict
    # return length: list of current words' length
    # rtype: list
    def getlength(self,currentdict):
        wordlist=self.cleandic(currentdict)
        length = []
        for word in wordlist:
            length.append(len(word))
        return length

    #deal the dictionary library
    #input file: words dictionary getting from internet
    #input type:str
    #return worddict: dictionary which key=length of words, value=words
    #rtype: dictionary
    def processdict(self,file):
        worddict = {}
        with open(file, 'r', encoding='utf-8') as f:
            f1 = f.read().split()
            for line in f1:
                try:
                    worddict[len(line)].append(line)
                except:
                    worddict[len(line)] = [line]
        return worddict
    # update current using dictionary
    # input worddict: the whole dictionary using to guess
    # input wordlist: list of guessing words in current status
    # input alpha: letter has guessed in the current round
    # input type: dict,list,str
    # return new_dict: the whole dictionary updated version
    # rtype: dict
    def updatedic(self,worddict,wordlist,alpha):
        new_dict={}
        for word in wordlist:
            word=word.upper()
            if alpha in word:
                index=0
                ind=[]
                while index<len(word):
                    index=word.find(alpha,index)
                    if index==-1:
                        break
                    ind.append(index)
                    index+=1
                leng=len(ind)
                if leng == 1:
                    for words in worddict[len(word)]:
                        words=words.upper()
                        if words[ind[0]] == alpha:
                            try:
                                new_dict[len(word)].append(words)
                            except:
                                new_dict[len(word)] = [words]
                        else:
                            pass
                else:
                    for words in worddict[len(word)]:
                        if words[ind[0]] == alpha:
                            try:
                                new_dict[len(word)].append(words)
                            except:
                                new_dict[len(word)] = [words]
                    for i in ind[1:]:
                        for words in new_dict[len(word)]:
                            if words[i] != alpha:
                                new_dict[len(word)].remove(words)
            else:
                for words in worddict[len(word)]:
                    try:
                        new_dict[len(word)].append(words)
                    except:
                        new_dict[len(word)]=[words]
                #new_dict[len(word)] = worddict[len(word)]
        return new_dict
    # update current letter probability
    # input usestr: the str of letter which has not been guessed
    # input length: list of guessing words' length
    # input new_dict: the updated whole dict
    # return frequentlist: list ordered in probability of letter may show
    # rtype: list
    def letterpro(self,usestr,length,new_dict):
        frequent={}
        for i in range(len(usestr)):
            count1 = 0
            count2 = 0
            for j in range(len(length)):
                for word in new_dict[length[j]]:
                    count2 += 1
                    if usestr[i] in word:
                        count1 += 1
            frequent[usestr[i]] = count1 / count2
        frequentlist = sorted(frequent.items(), key=lambda item: item[1], reverse=True)
        frequentlist = [a[0] for a in frequentlist]
        return frequentlist

class RequestManager:
    # http visit
    # input mail: mail address using to get package from web service
    def __init__(self,mail):
        self.mail=mail
    # get json package from web service
    # In case of timeout, the function has three chances to retry
    # return currentdict: First package from web service
    # rtype: dict
    def getjsonpac(self):
        i=0
        while i<3:
            try:
                r=requests.get('http://gallows.hulu.com/play?code='+self.mail,timeout=5)
                currentdict=js.loads(r)
                return currentdict
            except requests.exceptions.RequestException:
                i += 1

    # get json package updated from web service
    # input token: the id of this game
    # input guess: the letter now guessing
    # input type: int, str
    # return updatedict: new updated package
    # rtype: dict
    def updatejsonpac(self,token,guess):
        i=0
        while i<3:
            try:
                r = requests.get(
                    "http://gallows.hulu.com/play?code={}&token={}&guess={}".format(self.mail, token, guess))
                updatedict = js.loads(r)
                return updatedict
            except requests.exceptions.RequestException:
                i += 1
class RoundManager:
    # mail address and whole dictionary using in current round
    # input mail: mail address using to get package from web service
    # input round: cur
    def __init__(self, mail,round):
        self.mail=mail
        self.round=round

    def Init(self):
        ...
    def Run(self):
        frequencylist = ['e', 'a', 'o', 'i', 'u', 't', 's', 'r', 'n', 'h', 'l', 'd', 'c', 'm', 'f', 'p', 'g', 'w', 'y',
                         'b', 'v', 'k', 'x', 'j', 'q', 'z']
        DM=DictManager()
        worddict=DM.processdict('words.txt')
        RM=RequestManager(self.mail)
        currentdic=RM.getjsonpac()#first package get
        status=currentdic['status']
        str='abcdefghijklmnopqrstuvwxyz'
        length=DM.getlength(currentdic)
        alreadyguess=[]
        while status=='Alive':
            text = currentdic['state']
            if alreadyguess==[]:#make first guess
                if 1 in length:
                    firstguess = 'a'
                else:
                    firstguess = 'e'
                currentdic = RM.updatejsonpac(currentdic['token'], firstguess)
                status=currentdic['status']
                if status!='Alive':
                    decision=self.statuschoose(status,self.round)
                    return decision
                if text==currentdic['state']:
                    alreadyguess.append(firstguess)
                    frequencylist.remove(firstguess)
                    splitlist = str.split(firstguess)
                    if len(splitlist) == 1:
                        str = splitlist[0]
                    else:
                        str = splitlist[0] + splitlist[1]
                else:
                    wordlist = DM.cleandic(currentdic)
                    worddict = DM.updatedic(worddict, wordlist, firstguess)
                    splitlist = str.split(firstguess)
                    if len(splitlist) == 1:
                        str = splitlist[0]
                    else:
                        str = splitlist[0] + splitlist[1]
                    frequencylist=DM.letterpro(str,length,worddict)
                    alreadyguess.append(firstguess)
            elif alreadyguess!=[]:#make continue guess
                continueguess=frequencylist[0]
                currentdic=RM.updatejsonpac(currentdic['token'],continueguess)
                status = currentdic['status']
                if status!='Alive':
                    decision=self.statuschoose(status,self.round)
                    return decision
                if text==currentdic['state']:
                    alreadyguess.append(continueguess)
                    frequencylist.remove(continueguess)
                    splitlist=str.split(continueguess)
                    if len(splitlist)==1:
                        str=splitlist[0]
                    else:
                        str = splitlist[0] + splitlist[1]
                else:
                    wordlist=DM.cleandic(currentdic)
                    worddict=DM.updatedic(worddict,wordlist,continueguess)
                    splitlist = str.split(continueguess)
                    if len(splitlist) == 1:
                        str = splitlist[0]
                    else:
                        str = splitlist[0] + splitlist[1]
                    frequencylist = DM.letterpro(str, length, worddict)
                    alreadyguess.append(continueguess)

    def statuschoose(self,status,round):
        while status=='Dead':
            print('In round {0}, you lose the game!'.format(round))
            return False

        while status=='Free':
            print('In round {0}, you win the game!'.format(round))
            return True


class RunManager():
    def __init__(self, mail, round):
        self.mail = mail
        self.round = round

    def Process(self):
        f=0
        for i in range(1,self.round+1):
            RoM=RoundManager(self.mail,i)
            success = RoM.Run()
            if not success:
                f+=1
        return f


if __name__=='__main__':
    mail,round='jiayulin@usc.edu','2'
    if mail!='jiayulin@usc.edu':
        print('The email you enter is invaild!')
    elif round.isdigit()!=True or int(round)<=0:
        print('The number of rounds you enter is invaild!')
    else:
        round=int(round)
        RunM=RunManager(mail,round)
        Winrounds=round-RunM.Process()
        winrate=Winrounds/round
        print('You finish {0} rounds game with the {1} winrate'.format(round,winrate))
