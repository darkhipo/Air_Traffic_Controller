"""
This file contains the cores of this project such as Brute Force and SLS algorithms. These algorithms are used to get the best FlightPlan.
"""

import FlightPlan
import numpy
import random
import ParameterCore
import Flight
import FlightCombinator


def randSplit(wSize, candidates):                                     # public static FlightPlan randSplit(Integer wSize, List<Flight> candidates) {
    """
    Randomly choose some of the candidates

    Args:
        wSize: int. number of candidate needed to be chosen
        candidates: list. the list of Flight that needed to be randomly splitted.

    Return:
        [fp: FlightPlan, candidates: list]
    """
    numpy.random.shuffle(candidates)                                        # Collections.shuffle(candidates);
    flist = list()                                                          # List<Flight> flist = new ArrayList<Flight>();
    for i in range(0, wSize):                                               # for (int i = 0; i < wSize; i++) {
        flist.append(candidates[i])                                         # flist.add(candidates.get(i));
    candidates = [x for x in candidates if x not in flist]                  # candidates.removeAll(flist);
    fp = FlightPlan.FlightPlan(flist)                                                  # FlightPlan fp = new FlightPlan(flist);
    return fp                                                               # return fp;

def ordSplit(wSize, candidates):                                            # public static FlightPlan ordSplit(Integer wSize, List<Flight> candidates) {
    """
    Choose from those have highest rewards.

    Args:
        wSize: int. number of candidate needed to be chosen
        candidates: list. the list of Flight that needed to be randomly splitted.
    Return:
        [fp: FlightPlan, candidates: list]
    """
    insertionSort(candidates)                                               # Collections.sort(candidates);
    candidates.reverse()                                                    # Collections.reverse(candidates);
    flist = list()                                                          # List<Flight> flist = new ArrayList<Flight>();
    for i in range(0, wSize):                                               # for (int i = 0; i < wSize; i++) {
        flist.append(candidates[i])                                         # flist.add(candidates.get(i));
    candidates = [x for x in candidates if x not in flist]                  # candidates.removeAll(flist);
    fp = FlightPlan.FlightPlan(flist)                                       # FlightPlan fp = new FlightPlan(flist);
    return [fp, candidates]                                                 # return fp;


class FlightPlanCoordinator:                                                               # public class FlightPlanCoordinator {
    def __init__(self, fp, candidates):

        # self.waterFallSize = 0                                                           # private Integer      waterFallSize;
        # self.baseFlightPlan = FlightPlan()                                               # private FlightPlan   baseFlightPlan;
        # self.random = random.random()                                                    # private Random       random;
        # self.coordinates = []                                                            # private List<Flight> candidates;
        # self.temperature = 0.0                                                           # private Double       temperature;
        # self.candidates = list()

        self.random = random.Random()                                                       # this.random = new Random();
        self.baseFlightPlan = fp                                                            # this.baseFlightPlan = fp;
        self.waterFallSize = fp.size()                                                      # this.waterFallSize = fp.size();
        if candidates != None: self.candidates = candidates                                 # this.candidates = (candidates != null) ? Collections.synchronizedList(candidates) : new ArrayList<Flight>();
        self.temperature = ParameterCore.ParameterCore().PROB_RANDOR_BASE                   # this.temperature = ParameterCore.PROB_RANDOR_BASE;


    def cloneCandidates(self):                                                  # private List<Flight> cloneCandidates() {
        """
        Return:
            candid: a list of Flight
        """
        candid = list()                                                         # List<Flight> candid = Collections.synchronizedList(new ArrayList<Flight>());
        for f in self.candidates:                                               # for (Flight f : this.candidates) {
            candid.append(Flight.Flight(f))                                     # candid.add(new Flight(f));
        return candid                                                           # return candid;





    ''' ordSplit should be defined outside the class because this is a static function, nothing to do with self '''
    # def ordSplit(self, wSize, candidates):                                    # public static FlightPlan ordSplit(Integer wSize, List<Flight> candidates) {
    #     candidates.sort()                                                     # Collections.sort(candidates);
    #     candidates.reverse()                                                  # Collections.reverse(candidates);
    #     flist = list()                                                        # List<Flight> flist = new ArrayList<Flight>();
    #     for i in range(0, wSize):                                             # for (int i = 0; i < wSize; i++) {
    #         flist.append(candidates[i])                                       # flist.add(candidates.get(i));
    #     candidates = [x for x in candidates if x not in flist]                # candidates.removeAll(flist);
    #     fp = FlightPlan(flist)                                                # FlightPlan fp = new FlightPlan(flist);
    #     return fp                                                             # return fp;


    def runSLS(self):                                                           # public FlightPlan runSLS() {
        """
        Return:
             incumbent: FlightPlan generated by sls()
        """
        incumbent = self.sls()                                                  # FlightPlan incumbent = sls();
        if incumbent == None:                                                   # if (incumbent == null) {
            raise AssertionError()                                              # throw new AssertionError();
        return incumbent                                                        # return incumbent;


    def sls(self):
        """
        Use SLS to estimate the best FlightPlan it could get.

        Return:
            incumbent: FlightPlan
        """
        incumbent = self.baseFlightPlan.cloneFlightPlan()
        incumbentScore = incumbent.getExpectedValue()
        improvement = incumbentScore
        candid = self.cloneCandidates()

        if (len(candid) + incumbent.size()) < ParameterCore.ParameterCore().BRUTE_BOUND:    # if ((candid.size() + incumbent.size()) < ParameterCore.BRUTE_BOUND) {
            return self.runBruteForce()                                                     # return runBruteForce();

        while improvement > ParameterCore.ParameterCore().IMPROVEMENT_THRESHOLD:            # while (improvement.compareTo(ParameterCore.IMPROVEMENT_THRESHOLD) > 0) {
            improvement = 0.0                                                               # improvement = 0.0;
            for i in range(0, ParameterCore.ParameterCore().LOCAL_SEARCH_WINDOW):           # for (int i = 0; i < ParameterCore.LOCAL_SEARCH_WINDOW; i++) {
                if len(candid) > ParameterCore.ParameterCore().MIN_FLIGHTS_TO_TRY_IMPROVE:  # if (candid.size() > ParameterCore.MIN_FLIGHTS_TO_TRY_IMPROVE) {
                    swapInIndex = random.randrange(len(candid) - 1)                    # Integer swapInIndex = this.random.nextInt(candid.size() - 1);
                    swapOutIndex = random.randrange(incumbent.size() - 1)              # Integer swapOutIndex = this.random.nextInt(incumbent.size() - 1);
                    fpCandidate = incumbent.cloneFlightPlan()                               # FlightPlan fpCandidate = incumbent.cloneFlightPlan();

                    swappedIn = candid[swapInIndex]                                         # Flight swappedIn = candid.get(swapInIndex);
                    swappedOut = fpCandidate.get(swapOutIndex)                              # Flight swappedOut = fpCandidate.get(swapOutIndex);
                    fpCandidate.set(swapOutIndex, swappedIn)                                # fpCandidate.set(swapOutIndex, swappedIn);

                    if random.random() < self.temperature:                                  # if (random.nextDouble() < this.temperature) {
                        self.subSeqShuffle(fpCandidate)                                     # subSeqShuffle(fpCandidate);

                    candScore = fpCandidate.getExpectedValue()                              # Double candScore = fpCandidate.getExpectedValue();
                    if incumbentScore < candScore:                                          # if (incumbentScore.compareTo(candScore) < 0) {
                        improvement = max(improvement, candScore - incumbentScore)          # improvement = Math.max(improvement, candScore - incumbentScore);
                        incumbent = fpCandidate                                             # incumbent = fpCandidate;
                        incumbentScore = candScore                                          # incumbentScore = candScore;
                        candid.remove(swappedIn)                                   # this.candidates.remove(swappedIn);
                        candid.append(swappedOut)                                  # this.candidates.add(swappedOut);

                    else:                                                                   # else {
                        swapInIndex = random.randrange((incumbent.size()) - 1)         # Integer swapInIndex = this.random.nextInt(incumbent.size() - 1);
                        swapOutIndex = random.randrange((incumbent.size()) - 1)        # Integer swapOutIndex = this.random.nextInt(incumbent.size() - 1);
                        while (swapOutIndex == swapInIndex and (incumbent.size()) > 1):     # while (swapOutIndex == swapInIndex && incumbent.size() > 1) {
                            swapOutIndex = random.randrange((incumbent.size()) - 1)    # swapOutIndex = this.random.nextInt(incumbent.size() - 1);
                        fpCandidate = incumbent.cloneFlightPlan()                           # FlightPlan fpCandidate = incumbent.cloneFlightPlan();

                        swappedIn = fpCandidate.get(swapInIndex)                            # Flight swappedIn = fpCandidate.get(swapInIndex);
                        swappedOut = fpCandidate.get(swapOutIndex)                          # Flight swappedOut = fpCandidate.get(swapOutIndex);

                        fpCandidate.set(swapOutIndex, swappedIn)                            # fpCandidate.set(swapOutIndex, swappedIn);
                        fpCandidate.set(swapInIndex, swappedOut)                            # fpCandidate.set(swapInIndex, swappedOut);

                        if random.random() < self.temperature:                              # if (random.nextDouble() < this.temperature) {
                            self.subSeqShuffle(fpCandidate)                                 # subSeqShuffle(fpCandidate);

                        candScore = fpCandidate.getExpectedValue()                          # Double candScore = fpCandidate.getExpectedValue();
                        if incumbentScore < candScore:                                      # if (incumbentScore.compareTo(candScore) < 0) {
                            improvement = max(improvement, candScore - incumbentScore)      # improvement = Math.max(improvement, candScore - incumbentScore);
                            incumbent = fpCandidate                                         # incumbent = fpCandidate;
                            incumbentScore = candScore                                      # incumbentScore = candScore;

                    self.temperature = ((ParameterCore.ParameterCore().PROB_RANDOR_BASE - ParameterCore.ParameterCore().PROB_RANDOR_MIN)
                                        - (improvement / incumbentScore)) + ParameterCore.ParameterCore().PROB_RANDOR_MIN               # this.temperature = ((ParameterCore.PROB_RANDOR_BASE - ParameterCore.PROB_RANDOR_MIN) -
                                                                                                                                        # (improvement / incumbentScore)) + ParameterCore.PROB_RANDOR_MIN;
                    if ParameterCore.ParameterCore().DEBUG < 0:                                                                         # if (ParameterCore.DEBUG < 0) {
                        print(improvement , " " , (1.0 - (improvement / incumbentScore)) , " " , self.temperature)      # System.out.println(improvement + " " + (1.0 - (improvement / incumbentScore)) + " " + temperature);
        print("NO BFS Improvement!")                                                                                    # System.out.println("NO BFS Improvement!");

        return incumbent                                                                                                # return incumbent;


    def subSeqShuffle(self, fpCandidate):                                                                               # private void subSeqShuffle(FlightPlan fpCandidate) {
        """
        Randomly shuffle the FlightPlan candidates
        """
        swapOneIdx = random.randint(0, (fpCandidate.size()) - 1)                                                        # Integer swapOneIdx = this.random.nextInt(fpCandidate.size() - 1);
        swapTwoIdx = random.randint(0, (fpCandidate.size()) - 1)                                                        # Integer swapTwoIdx = this.random.nextInt(fpCandidate.size() - 1);
        while (swapOneIdx == swapTwoIdx and (fpCandidate.size()) > 1):                                                  # while (swapOneIdx == swapTwoIdx && fpCandidate.size() > 1) {
            swapOneIdx = random.randint(0, (fpCandidate.size()) - 1)                                                    # swapOneIdx = this.random.nextInt(fpCandidate.size() - 1);
        numpy.random.shuffle(fpCandidate.getAsList()[min(swapOneIdx, swapTwoIdx):max(swapOneIdx, swapTwoIdx)])          # Collections.shuffle(fpCandidate.getAsList().subList(Math.min(swapOneIdx, swapTwoIdx),
                                                                                                                        # Math.max(swapOneIdx, swapTwoIdx)));


    def runBruteForce(self, *args):                                                                                     # public FlightPlan runBruteForce(List<Flight> allFlights) {
                                                                                                                        # if allFlights.size() > ParameterCore.BRUTE_BOUND) {
                                                                                                                        # throw new AssertionError("Brute Force Bound Exceeded");
        """
        Run the Brute Force when the number of flights does not exceed the Brute_Bond defined in ParameterCore.py
        """
        if len(args) == 0:
            FP = FlightPlan.FlightPlan(self.baseFlightPlan)
            allFlights = FP.getAsList()                                                                                 # List<Flight> allFlights = new FlightPlan(this.baseFlightPlan).getAsList();
            allFlights.extend(self.cloneCandidates())                                                                   # allFlights.addAll(cloneCandidates());
            return self.runBruteForce(allFlights)                                                                       # return runBruteForce(allFlights);
        else:
            allFlights = args[0]
            minFlights = min(self.waterFallSize, len(allFlights))                                                             # Integer minFlights = Math.min(this.waterFallSize, allFlights.size());
            fc = FlightCombinator.FlightCombinator(allFlights, minFlights)                                              # FlightCombinator fc = new FlightCombinator(allFlights, minFlights);

            bestPlan = FlightPlan.FlightPlan(allFlights[0:minFlights])                                                             # FlightPlan bestPlan = new FlightPlan(allFlights.subList(0, minFlights));

            bestPlanScore = bestPlan.getExpectedValue()                                                                 # Double bestPlanScore = bestPlan.getExpectedValue();
            changed = True
            while fc.has_next():                                                                                        # for (FlightPlan fp : fc) {
                fp = FlightPlan.FlightPlan(fc.get_next())
                expVal = fp.getExpectedValue()                                                                          # Double expVal = fp.getExpectedValue();

                if bestPlanScore < expVal:                                                                              # if (bestPlanScore.compareTo(expVal) < 0) {
                    bestPlan = fp                                                                                       # bestPlan = fp;
                    bestPlanScore = expVal                                                                              # bestPlanScore = expVal;
                    changed = True
                if ParameterCore.ParameterCore().DEBUG > 0 and changed == True:                                                                 # if (ParameterCore.DEBUG > 0) {
                    print(bestPlan.get(0).getPlacementToken(), " " , bestPlan.getExpectedValue())                          # System.out.println(bestPlan.get(0).getPlacementToken() + " " + bestPlan.getExpectedValue());
                    print(bestPlan.toString())                                                                                         # System.out.println(bestPlan);
                    changed = False
            return bestPlan                                                                                             # return bestPlan;


def insertionSort(alist):
    """
    Use insertion sort to sort Flight

    """
    for index in range(1, len(alist)):

        currentvalue = alist[index]
        position = index

        while position > 0 and currentvalue.compareTo(alist[position - 1]) < 0:
            alist[position] = alist[position - 1]
            position = position - 1

        alist[position] = currentvalue





