import random
import math
import numpy
import sys
import ParameterCore
import Utils
import Placement


class CLI:                                                          # public class CLI
    def __init__(self):
        self.memo = dict()                                          # static HashMap<HashSet<String>, FlightPlan> memo
        return

    def runCLI(self, args):
        if len(args) < 4:                                           # if (args.length < 4)
            print(ParameterCore.ParameterCore().USAGE)              # System.out.println(ParameterCore.USAGE);
            print("Argument Error: There must be 4 arguments.")     # System.err.println("Argument Error: There must be 4 arguments.");
            exit()                                                  # System.exit(1);
        else:
            #try:
            self.control            = args[0]                        # control        		= args[0];
            self.waterfallSizeLimit = int(args[1])                   # waterfallSizeLimit   = Integer.valueOf(args[1]);
            self.inFileName         = args[2]                        # inFileName     		= args[2];
            self.outFileName        = args[3]                        # outFileName    		= args[3];
            self.allFlights         = None                           # List<Flight> allFlights 	  		= null;
            self.allPlacements      = None                           # List<Placement> allPlacements    = null;

            # except Exception as e:                                       # System.err.println("\nArgument Error: " + e.getMessage() + " "
            #     print("\nArgument Error: " + str(e))                     # + e.getLocalizedMessage() + " " + e.getCause());
            #     exit()

            # try:
            self.allFlights = Utils.Utils().readFlightsCSV(ParameterCore.ParameterCore().csv, self.inFileName)      # allFlights = Utils.readFlightsCSV(ParameterCore.csv, inFileName);
            # except Exception as e:
            #     print("Error reading from file: " + self.inFileName)                                                    # System.out.println("Error reading from file: " + inFileName);
            #     print("\nInput File Error: " + str(e))                                                                  # System.err.println("\nInput File Error: " + e.getMessage() + " "
            #     exit()                                                                                                  # + e.getLocalizedMessage() + " " + e.getCause());
            #                                                                                                             # e.printStackTrace();"""
            ### Preprocess input data START ###
            # Preprocess each flight plan. This fills in missing data items.
        Utils.Utils().preProcessFlights(self.allFlights)
        # Partition flights into Placements.
        self.allPlacements = Utils.Utils().partitionToPlacements(self.allFlights)
        # Lexicographic sort Placements.
        self.insertionSort(self.allPlacements)
        ### Preprocess input data END ###

        # Run Optimization Start
        Utils.Utils().optimizePlacements(self.waterfallSizeLimit, self.control, self.allPlacements)                     # Utils.optimizePlacements(waterfallSizeLimit, control, allPlacements);
        #  Run Optimization End #

        ### Output data after processing START ###
        writeList = list()                                                                                              # List<Flight> writeList = new ArrayList<Flight> ();
        for p in self.allPlacements:                                                                                    # for (Placement p: allPlacements){
            writeList.append(p.getFp().getAsList())                                                                     # writeList.addAll(p.getFp().getAsList());
            print(p.pid, " :::: ", p.fp.getExpectedValue())                                                             # System.out.println(p.pid + " :::: " + p.fp.getExpectedValue() );
        for x in writeList:
            for f in x:
                #print(x)
                print(f.toString())
        #Utils.Utils().writeFlightPlanCSV((ParameterCore.ParameterCore().csv, self.outFileName, writeList))              # Utils.writeFlightPlanCSV(ParameterCore.csv, outFileName, writeList);
        print(("Generated file [", self.outFileName, "]", " From data ", "[", self.inFileName, "]"))                    # System.out.println("Generated file ["+outFileName+"]" + " From data " + "[" + inFileName + "]");




    def getBinomial(self, n, p):                                    # public static int getBinomial(int n, double p)
        x = 0                                                       # int x = 0;
        for i in range(n):                                          # for(int i = 0; i < n; i++)
            if random.random() < p:                                 # if( Math.random( ) < p )
                x += 1                                              # x++;
        return x

    # current_time = int(time.time()*1000) + random.random()  ## static jdistlib.rng.MersenneTwister twister = new jdistlib.rng.MersenneTwister( System.currentTimeMillis() + (long) Math.random( ) );
    # random.seed(current_time)
    ################################## Need to be fixed here!

    def simRun(self, flight):
        reward = flight.getReward()                                                                                # Double reward           = flight.getReward();
        probSucc = flight.getProbability()                                                                         # Double probSucc         = flight.getProbability();
        costFlipFail = flight.getTimeAverageFailure()                                                              # Double costFlipFail     = flight.getTimeAverageFailure();
        costFlipSucc = flight.getTimeAverageSuccess()                                                              # Double costFlipSucc     = flight.getTimeAverageSuccess();
        costFlipFail_std = flight.getTimeStdDevFailure()                                                           # Double costFlipFail_std = flight.getTimeStdDevFailure();
        costFlipSucc_std = flight.getTimeStdDevSuccess()                                                           # Double costFlipSucc_std = flight.getTimeStdDevSuccess();
        logNormVar_S = math.log((math.pow(costFlipSucc_std, 2)/math.pow(costFlipSucc, 2)) + 1.0)         # Double logNormVar_S     = Math.log( (Math.pow(costFlipSucc_std,2)/Math.pow(costFlipSucc,2)) + 1.0);
        logNormMean_S = math.log(costFlipSucc) - (logNormVar_S/2.0)                                      # Double logNormMean_S    = Math.log(costFlipSucc) - (logNormVar_S/2.0);
        successDelay = numpy.random.lognormal(logNormMean_S, math.sqrt(logNormVar_S))                    # Double successDelay     = jdistlib.LogNormal.random( logNormMean_S, Math.sqrt( logNormVar_S ), twister );
        logNormVar_F = math.log((math.pow(costFlipFail_std, 2) / math.pow(costFlipFail, 2)) + 1.0)       # Double logNormVar_F     = Math.log( (Math.pow(costFlipFail_std,2) / Math.pow(costFlipFail,2)) + 1.0);
        logNormMean_F = math.log(costFlipFail)-(logNormVar_F/2.0)                                        # Double logNormMean_F    = Math.log( costFlipFail )-( logNormVar_F/2.0 );
        failureDelay = numpy.random.lognormal(logNormMean_F, math.sqrt(logNormVar_F))                    # Double failureDelay     = jdistlib.LogNormal.random( logNormMean_F, Math.sqrt( logNormVar_F ), twister );

        isSuccess = self.getBinomial(1, probSucc) > 0                                                         # boolean isSuccess = getBinomial(1, probSucc) > 0;

        if isSuccess:
            return [reward, successDelay]

        else:
            return [0.0, failureDelay]

    def calculateAverage(self, marks):
        _sum = 0.0
        if marks != []:
            for mark in marks:
                _sum += mark
            return float(_sum)/len(marks)
        return _sum



    def runCLISim(self, args):
        if len(args) < 4:  # if (args.length < 4)
            print(ParameterCore.ParameterCore().USAGE)  # System.out.println(ParameterCore.USAGE);
            print("Argument Error: There must be 4 arguments.")  # System.err.println("Argument Error: There must be 4 arguments.");
            exit()  # System.exit(1);
        else:
            # try:
            self.control = args[0]  # control        		= args[0];
            self.waterfallSizeLimit = int(args[1])  # waterfallSizeLimit   = Integer.valueOf(args[1]);
            self.inFileName = args[2]  # inFileName     		= args[2];
            self.outFileName = args[3]  # outFileName    		= args[3];
            self.allFlights = None  # List<Flight> allFlights 	  		= null;
            self.allPlacements = None  # List<Placement> allPlacements    = null;

            # except Exception as e:  # System.err.println("\nArgument Error: " + e.getMessage() + " "
            #     print("\nArgument Error: " + str(e))  # + e.getLocalizedMessage() + " " + e.getCause());
            #     exit()

            # try:
            self.allFlights = Utils.Utils().readFlightsCSV(ParameterCore.ParameterCore().csv, self.inFileName)  # allFlights = Utils.readFlightsCSV(ParameterCore.csv, inFileName);
            # except Exception as e:
            #     print(
            #     "Error reading from file: " + self.inFileName)  # System.out.println("Error reading from file: " + inFileName);
            #     print(
            #     "\nInput File Error: " + str(e))  # System.err.println("\nInput File Error: " + e.getMessage() + " "
            #     exit()  # + e.getLocalizedMessage() + " " + e.getCause());
            # e.printStackTrace();"""
            ### Preprocess input data START ###
            # Preprocess each flight plan. This fills in missing data items.
        Utils.Utils().preProcessFlights(self.allFlights)
        # Partition flights into Placements.
        self.allPlacements = Utils.Utils().partitionToPlacements(self.allFlights)
        # Lexicographic sort Placements.
        #print(type(self.allPlacements))
        self.insertionSort(self.allPlacements)
        ### Preprocess input data END ###


        cityCount = 0                           # int cityCount = 0;
        tMax = 0                                # double tMax = 0;
        packs = dict()                          # HashMap<Integer,RunData> packs = new HashMap<Integer,RunData> ();

        for p in self.allPlacements:                  # for (Placement p: allPlacements){
            packs.clear()                        # packs.clear(); ##is this necessary?
            for j in range(-1, p.getFp().size()):  # for (int j = -1; j < p.getFp().size(); j + +){
                pack = RunData()                 # RunData pack = new RunData();
                pack.window = j                  # pack.window = j;
                packs.update({j: pack})          # packs.put(j, pack);

                maxWindow = 5 # Integer maxWindow = 5;//p.getFp().size();
                drawStore = dict() # HashMap<String, Double[]> drawStore = new HashMap<String, Double[]>();
                for j in range(-1, maxWindow):                               # for ( int j=-1; j < maxWindow; j++ ){
                    if j > -1:                                               # if( j > -1 )
                        Utils.Utils().optimizePlacement(2147483647, self.control, p)     # Utils.optimizePlacement(Integer.MAX_VALUE, control, p);
                    else:
                        Utils.Utils().optimizePlacement(2147483647, self.control, p)     # Utils.optimizePlacement(Integer.MAX_VALUE, control, p);
                        if p.getFp().size() > 3:
                            random.shuffle(p.getFp().getAsList()[2:p.getFp().size()])   # Collections.shuffle( p.getFp().getAsList().subList(2, p.getFp().size()) )

                    rewards = []                         # ArrayList<Double> rewards = new ArrayList<Double> ();
                    visitsBeforeFailure = []             # ArrayList<Integer> visitsBeforeFailure = new ArrayList<Integer> ();
                    visitsBeforeSuccess = []             # ArrayList<Integer> visitsBeforeSuccess = new ArrayList<Integer> ();
                    pathLengthBeforeFailure = []         # ArrayList<Double> pathLengthBeforeFailure = new ArrayList<Double> ();
                    pathLengthBeforeSuccess = []         # ArrayList<Double> pathLengthBeforeSuccess = new ArrayList<Double> ();
                    timeAtLastFailure = []               # ArrayList<Double> timeAtLastFailure = new ArrayList<Double> ();
                    timeAtLastSuccess = []               # ArrayList<Double> timeAtLastSuccess = new ArrayList<Double> ();
                    failureCount = 0                     # Integer failureCount = 0;
                    successCount = 0                     # Integer successCount = 0;

                    for i in range(0, self.waterfallSizeLimit):              # for (int i=0; i<waterfallSizeLimit; i++)
                        cityCount = p.getFp().size()                      # cityCount = p.getFp().size();
                        tMax = p.getFp().getAsList()[0].getTimeMax()      # tMax = p.getFp().getAsList().get(0).getTimeMax();
                        myPlan = p.getFp().cloneFlightPlan()            # FlightPlan myPlan = p.getFp().cloneFlightPlan();
                        myTrip = []                                     # ArrayList<String> myTrip = new ArrayList<String> ( );
                        timeRemain = myPlan.getAsList()[0].getTimeMax() # double timeRemain = myPlan.getAsList().get(0).getTimeMax();
                        timeMax = myPlan.getAsList()[0].getTimeMax()    # double timeMax = myPlan.getAsList().get(0).getTimeMax();

                        doStop = False                                      # boolean doStop = false;
                        while not doStop:                                   # while( !doStop )
                            myL = ''                                        # String myL = "";
                            for f in myPlan.getAsList():                                # for (Flight f : myPlan)
                                myL += str(f.getFid()) + ' '                     # myL += f.getFid() + " ";

                            front = myPlan.getAsList()[1:]                    # Flight front = myPlan.getAsList().remove( 0 );
                            try:
                                key = front[i].getFid() + i                          # String key = front.getFid() + i;             ############################ key = front.getFid() + i
                            except IndexError:
                                pass
                            testArr = None                                    # Double testArr[] = null;
                            if key in drawStore.keys():                       # if ( drawStore.containsKey(key) )
                                testArr = drawStore[key]                      # testArr = drawStore.get(key);
                            else:
                                testArr = self.simRun(front[i])                    # testArr = simRun( front );                     ################ testArr = self.simRun(front)
                                drawStore.update({key:testArr})                 # drawStore.put(key, testArr);

                            prevTime = timeRemain                           # double prevTime = timeRemain;
                            timeRemain -= testArr[1]                        # timeRemain -= testArr[1];

                            try:
                                myTrip.append(front[i].getFid())                             # myTrip.add( front.getFid() );
                            except IndexError:
                                pass

                            if testArr[0] > 0.0 and timeRemain >= 0.0:                # if ( testArr[0] > 0.0 && timeRemain >= 0.0 )
                                rewards.append(testArr[0])                            # rewards.add( testArr[0] );
                                visitsBeforeSuccess.append(len(myTrip))               # visitsBeforeSuccess.add( myTrip.size() );
                                pathLengthBeforeSuccess.append(timeMax - timeRemain)  # pathLengthBeforeSuccess.add( timeMax - timeRemain );
                                timeAtLastSuccess.append(prevTime)                    # timeAtLastSuccess.add( prevTime );
                                successCount += 1                                     # successCount += 1;
                                doStop = True                                         # doStop = true;
                                break

                            elif myPlan.size() < 1 or timeRemain <= 0.0:                # else if ( myPlan.size() < 1 || timeRemain <= 0.0 )
                                rewards.append(0.0)                                   # rewards.add( 0.0 );
                                visitsBeforeFailure.append(len(myTrip))               # visitsBeforeFailure.add( myTrip.size() );
                                pathLengthBeforeFailure.append(timeMax - timeRemain)  # pathLengthBeforeFailure.add( timeMax - timeRemain );
                                timeAtLastFailure.append(prevTime)                    # timeAtLastFailure.add( prevTime );
                                failureCount += 1                                     # failureCount += 1;
                                doStop = True                                         # doStop = true;
                                break

                            if not doStop:                                            # if ( !doStop )
                                for f in myPlan.getAsList():                                      # for( Flight f : myPlan )
                                    f.setTimeMax(timeRemain)                          # f.setTimeMax( timeRemain )

                                if j > 0:                                             # if ( j > 0 )
                                    temp = Placement.Placement(front[i].getPlacementToken(), myPlan.cloneFlightPlan())     # Placement temp = new Placement( front.getPlacementToken(), myPlan.cloneFlightPlan() );
                                    Utils.Utils().optimizePlacement(j, "b", temp)                                       # Utils.optimizePlacement( j, "b", temp );
                                    best = temp.getFp()[0]                                                          # Flight best = temp.getFp().get(0);
                                    myPlan.getAsList().remove(best)                                         # myPlan.getAsList().remove(best);
                                    myPlan.getAsList().insert(0, best)                                       # myPlan.getAsList().add(0, best);

                        myL = ""                                                                             # String myL = "";
                        for s in myTrip:                                                                     # for (String s : myTrip)
                            myL += str(s) + " "                                                                   # myL += s + " ";
                        fname = self.inFileName[(self.inFileName.rfind('/') + 1) : len(self.inFileName)]        # String fname = inFileName.substring(inFileName.lastIndexOf('/') + 1, inFileName.length());

                    print("aa",packs)
                    print(packs[j])
                    rd = packs[j]                                                                            # RunData rd = packs.get(j);
                    rd.averageReward = self.calculateAverage(rewards)                                        # rd.averageReward = calculateAverage( rewards );
                    rd.averagePathLengthBeforeFailure = self.calculateAverage( pathLengthBeforeFailure )     # rd.averagePathLengthBeforeFailure = calculateAverage( pathLengthBeforeFailure );
                    rd.averagePathLengthBeforeSuccess = self.calculateAverage( pathLengthBeforeSuccess )     # rd.averagePathLengthBeforeSuccess = calculateAverage( pathLengthBeforeSuccess );
                    rd.averageTimeAtLastFail = self.calculateAverage( timeAtLastFailure )                    # rd.averageTimeAtLastFail = calculateAverage( timeAtLastFailure );
                    rd.averageTimeAtLastSuccess = self.calculateAverage( timeAtLastSuccess )                 # rd.averageTimeAtLastSuccess = calculateAverage( timeAtLastSuccess );
                    rd.averageVisitsBeforeFailure = self.calculateAverage( visitsBeforeFailure )             # rd.averageVisitsBeforeFailure = calculateAverage2( visitsBeforeFailure );
                    rd.averageVisitsBeforeSuccess = self.calculateAverage( visitsBeforeSuccess )             # rd.averageVisitsBeforeSuccess = calculateAverage2( visitsBeforeSuccess );
                    rd.failCount = failureCount                                                              # rd.failCount = failureCount;
                    rd.successCount = successCount                                                           # rd.successCount = successCount;

                    # for avg in rewards:
                    #      print("REW" + avg)                                                             # System.out.println("REW " + avg);
                    fname = self.inFileName[(self.inFileName.rfind('/') + 1) : len(self.inFileName)]       # String fname = inFileName.substring( inFileName.lastIndexOf('/') + 1, inFileName.length() );
                    outS = ""                                                                           # String outS = "";
                    outS += str(fname) + "," + str(rd.toString())                                                            # outS += fname + "," + rd ;

                    #try:                                                                            # try:
                    with open("result.txt", "w+")as out:                                        # PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(outFileName, true)));
                        out.write(outS)                                                         # out.println( outS );
                        out.flush()                                                             # out.flush();
                        out.close()                                                             # out.close();
                        print(outS)                                                             # System.out.println( outS );
                        #except Exception as e:                                                          # catch (IOException e) {
                        #    print(e)                                                                    # e.printStackTrace();


    def insertionSort(self, alist):
        for index in range(1, len(alist)):

            currentvalue = alist[index]
            position = index

            while position > 0 and currentvalue.compareTo(alist[position - 1]) < 0:
                alist[position] = alist[position - 1]
                position = position - 1

            alist[position] = currentvalue









class RunData:
    def __init__(self):
        self.window = 0                              # public Integer window;
        self.averageReward = 0                       # public Double averageReward;
        self.averageVisitsBeforeFailure = 0          # public Double averageVisitsBeforeFailure;
        self.averageVisitsBeforeSuccess = 0          # public Double averageVisitsBeforeSuccess;
        self.averagePathLengthBeforeFailure = 0      # public Double averagePathLengthBeforeFailure;
        self.averagePathLengthBeforeSuccess = 0      # public Double averagePathLengthBeforeSuccess;
        self.averageTimeAtLastFail = 0               # public Double averageTimeAtLastFail;
        self.averageTimeAtLastSuccess = 0            # public Double averageTimeAtLastSuccess;
        self.failCount = 0                           # public Integer failCount;
        self.successCount = 0                        # public Integer successCount;

    def toString(self):
        return (self.window, ",", self.averageReward, ",", self.averageVisitsBeforeFailure, ",",
                self.averageVisitsBeforeSuccess, ",", self.averagePathLengthBeforeFailure, ",",
                self.averagePathLengthBeforeSuccess, ",", self.averageTimeAtLastFail, ",",
                self.averageTimeAtLastSuccess, ",", self.failCount, ",", self.successCount)










