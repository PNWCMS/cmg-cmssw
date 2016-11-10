import PhysicsTools.Heppy.loadlibs
import ROOT

class KalmanMuonCorrector:
    def __init__(self, calibration, isMC, isSync=False, smearMode="none"):
        self.kamuca = ROOT.KalmanMuonCalibrator(calibration)
        self.isMC = isMC
        self.isSync = isSync
        self.smearMode = smearMode
    def correct(self, mu, run):
        newPt = self.kamuca.getCorrectedPt(mu.pt(), mu.eta(), mu.phi(), mu.charge())
        if self.isMC: # new we do the smearing
            if self.isSync:
                newPt = self.kamuca.smearForSync(newPt, mu.eta())
            elif self.smearMode == "none" or self.smearMode == None:
                pass
            else:
                newPt = self.kamuca.smear(newPt, mu.eta())

        newPtErr = newPt * self.kamuca.getCorrectedError(newPt, mu.eta(), mu.ptErr()/newPt)

        newP4 = ROOT.math.PtEtaPhiMLorentzVector(newPt, mu.eta(), mu.phi(), mu.mass())
        mu.setP4(newP4)
        # changed by Hengne Li, see comments in Muon.py
        #mu._ptErr = newPtErr
        mu.setPtErr(newPtErr)

    def correct_all(self, mus, run):
        for mu in mus:
            self.correct(mu, run)

if __name__ == '__main__':
    kamuka = KalmanMuonCorrector("MC_76X_13TeV", True)
