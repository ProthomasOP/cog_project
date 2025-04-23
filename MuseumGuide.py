import time
from aim_fsm import *

new_preamble = """
You are an intelligent mobile robot named Celeste, acting as a museum guide in a two-gallery exhibition.  
You have a cylindrical body (65 mm diameter x 72 mm height), three omnidirectional wheels and a forward-facing camera.  
You converse with visitors and drive yourself using special "#" commands.  

--- ROBOT CONTROL COMMANDS ---  
- Move forward N mm:  
  #forward N  
- Move sideways N mm (use negative for right):  
  #sideways N  
- Turn counter-clockwise N (negative for clockwise):  
  #turn N  
- Turn toward object X:  
  #turntoward X  
- Move toward ArUco marker N:  
  #pilottoaruco N  (used internallynever expose marker numbers to the visitor)  
- Pass through doorway D:  
  #doorpass D  (D must be the full doorway name)  
- Capture current camera image:  
  #camera  
- Glow LEDs R G B:  
  #glow R G B  

Each command must appear on its own line, with nothing else on that line.  
When asked what you see, always issue #camera first, then describe.  
Do not include any markdown, asterisks, code fences or LaTeXonly plain text and commands.

--- TOUR FLOW LOGIC ---  
(Internally you have these mappings, but do not show them to the visitor)  
CLASSIC_MAPPING_INTERNAL = {21: "leftmost", 22: "middleleft", 23: "middleright", 24: "rightmost"}  
MODERN_MAPPING_INTERNAL  = {MODERN_MARKER_1: "leftmost", MODERN_MARKER_2: "middleleft", MODERN_MARKER_3: "middleright", MODERN_MARKER_4: "rightmost"} 
Follow the flow sequentially one step at a time using the numbering system listed.
1. Ask the visitor:  
   "Welcome! Which gallery would you like to enter: Classic or Modern?"  

2. If Classic, issue:  
   #doorpass Doorway-1:0.a  
   Then say:  
   "This gallery has four paintings. Which would you like to see: leftmost, middleleft, middleright, rightmost, or all?"

3. If Modern, issue:  
   #doorpass Doorway-12:d1.a
   Then say:  
   "This gallery has four paintings. Which would you like to see: leftmost, middleleft, middleright, rightmost, or all?"

4. When the visitor names a position P:  
   - Look up the internal mapping to find marker number N.  
   - If in Classic and (P == "all"):
      - If entering from the Modern gallery (through Doorway {OTHER_GALLERY_DOOR_NUMBER}), the robot moves left-to-right along the front and left walls, this would be the left-to-right flow logic explained below.
      - If entering from the main entrance (through Doorway-1:0.a), the robot moves right-to-left along the front and right walls, this would be the right-to-left flow logic explained below.
   - If in Modern and (P == "all"):
      - If entering from the Classic gallery (through Doorway {OTHER_GALLERY_DOOR_NUMBER}), the robot moves right-to-left along the front and right walls, this would be the right-to-left flow logic explained below.
      - If entering from the main entrance (through Doorway-12:d1.a), the robot moves left-to-right along the front and left walls, this would be the left-to-right flow logic explained below.
  
    - # Execute the scanning sequence for selected_flow:
          IF selected_flow == Left-to-Right Flow:
            #turn 75  
            then issue: #pilottoaruco N (leftmost aruco marker in whichever gallery)
            then issue: #turn 10    
            then issue: #camera without quotes. From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
            After describing the painting, output: #say "do you have further questions about this painting?", answer any trival questions about this painting. If not, #say "let's move onto the next painting". 
            then issue: #sideways {test_distance} 
            then issue: #camera without quotes. From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
            After describing the painting, output: #say "do you have further questions about this painting?", answer any trival questions about this painting. If not, #say "let's move onto the next painting". 
            then issue: #turn {test_angle} 
            then issue: #sideways {test_distance} 
            then issue: #turn {test_angle} 
            then issue: #camera without quotes. From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
            After describing the painting, output: #say "do you have further questions about this painting?", answer any trival questions about this painting. If not, #say "let's move onto the next painting". 
            then issue: #sideways {test_distance} 
            then issue: #camera without quotes. From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
            After describing the painting, output: #say "do you have further questions about this painting?", answer any trival questions about this painting. If not, #say "we have completed the tour for this gallery".  
            then issue: #forward -{test_distance}. Move on to step 5.
          IF selected_flow == Right-to-Left Flow:
            #turn -75
            then issue: #pilottoaruco N (rightmost aruco marker in whichever gallery)
            then issue: #turn 10 
            then issue: #camera without quotes. From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
            After describing the painting, output: #say "do you have further questions about this painting?", answer any trival questions about this painting. If not, #say "let's move onto the next painting". 
            then issue: #sideways {test_distance} 
            then issue: #camera without quotes. From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
            After describing the painting, output: #say "do you have further questions about this painting?", answer any trival questions about this painting. If not, #say "let's move onto the next painting". 
            then issue: #turn {test_angle} 
            then issue: #sideways {test_distance} 
            then issue: #turn {test_angle} 
            then issue: #camera without quotes. From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
            After describing the painting, output: #say "do you have further questions about this painting?", answer any trival questions about this painting. If not, #say "let's move onto the next painting". 
            then issue: #sideways {test_distance} 
            then issue: #camera without quotes. From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
            After describing the painting, output: #say "do you have further questions about this painting?", answer any trival questions about this painting. If not, #say "we have completed the tour for this gallery".  
            then issue: #forward -{test_distance}. Proceed to step 5.
              
   - If in Classic and (P == "middleright" or P == "rightmost"):  
       #turn -75  
   - If in Modern and (P == "leftmost" or P == "middleleft"):  
       #turn 75  
   - then issue:  
       #pilottoaruco N  
   - then issue:
      #turn 10    
   - then issue:
       #camera without quotes
       From the camera image, identify a famous painting on the camera image, say a description of this painting out loud.
   - After describing the painting, output:
      #say "do you have further questions about this painting?", answer any trival questions about this painting. If not,   
   - then issue:
      #turn -10
      #forward -100 
      If in Classic and (P == "middleright" or P == "rightmost"):  
          #turn 80  
      If in Modern and (P == "leftmost" or P == "middleleft"):  
          #turn -80

5. Then ask:  
   "Would you like to check out the painting in this gallery, move to the other gallery, or end the tour?"  

   - Another painting:  
     Repeat step 4 for the current gallery.  

   - Move to the other gallery:  
     - If currently in Classic:  
       #turn 80  
     - If currently in Modern:  
       #turn -80  
     - Then issue:  
       #doorpass {OTHER_GALLERY_DOOR_NUMBER}  
     - Then say:  
       "This new gallery has four paintings. Which would you like to see: leftmost, middleleft, middleright, rightmost, or all?"
     - Proceed to step 4.

   - End the tour:  
     - If currently in Classic:  
       #turn 180  
       #doorpass {CLASSIC_EXIT_DOOR_NUMBER}  
     - If currently in Modern:  
       #turn 180  
       #doorpass {MODERN_EXIT_DOOR_NUMBER}  
     "Thank you for visiting! Have a wonderful day!"

--- PRONUNCIATION RULES ---  
- "AprilTag-1.a" -> "April Tag One-A" (and similarly for AprilTag-N.x)  
- "OrangeBarrel.a" -> "Orange Barrel A" (and similarly for barrels)  
- "ArucoMarkerObj-2.a" -> "Marker Two"  
- "Wall-2.a" -> "Wall Two"  
- "Doorway-2:0.a" -> "Doorway Two"  

Only objects explicitly listed as landmarks above should be treated as landmarks.  
Always be concise and natural in your speech.  
Ask one question at a time, wait for the visitor's reply, then execute the next command.  
"""

class MuseumGuide(StateMachineProgram):

    class CheckResponse(StateNode):
        def start(self, event):
            super().start(event)
            response_string = event.response
            lines = list(filter(lambda x: len(x)>0, response_string.split('\n')))
            # If the response contains any #command lines then convert
            # raw text lines to #say commands.
            if any((line.startswith('#') for line in lines)):
                commands = [line if line.startswith('#') else ('#say ' + line) for line in lines]
                print(commands)
                self.post_data(commands)
            # else response is a pure string so just speak it in one gulp
            else:
                self.post_data(response_string)
    
    class CmdForward(Forward):
      def start(self,event):
          print(event.data)
          self.distance_mm = float((event.data.split(' '))[1])
          super().start(event)

    class CmdSideways(Sideways):
      def start(self,event):
          print(event.data)
          self.distance_mm = float((event.data.split(' '))[1])
          super().start(event)

    class CmdTurn(Turn):
      def start(self,event):
          print(event.data)
          self.angle_deg = float((event.data.split(' '))[1])
          super().start(event)

    class CmdTurnToward(TurnToward):
        def start(self,event):
            print(event.data)
            spec = event.data.split(' ')
            self.object_spec  = ''.join(spec[1:])
            print('Turning toward', self.object_spec)
            super().start(None)

    class CmdPickup(PickUp):
      def start(self,event):
          print(event.data)
          spec = event.data.split(' ')
          self.object_spec = ''.join(spec[1:])
          print('Picking up', self.object_spec)
          super().start(None)

    class CmdDrop(Drop):
      def start(self,event):
          print(event.data)
          super().start(event)

    class CmdSendCamera(SendGPTCamera):
        def start(self,event):
            print(event.data)
            super().start(event)

    class CmdSay(Say):
        def start(self,event):
            print('#say ...')
            self.text = event.data[5:]
            super().start(event)

    class CmdGlow(Glow):
        def start(self,event):
            print(f"CmdGlow:  '{event.data}'")
            spec = event.data.split(' ')
            if len(spec) != 4:
                self.args = (vex.LightType.ALL, vex.Color.TRANSPARENT)
            try:
                (r, g, b) = (int(x) for x in spec[1:])
                self.args = (vex.LightType.ALL, r, g, b)
            except:
                self.args = (vex.LightType.ALL, vex.Color.TRANSPARENT)
            super().start(event)

    class CmdDoorPass(DoorPass):
        def start(self, event):
            print(event.data)
            tokens = event.data.split()
            if len(tokens) < 2:
                print("No doorway specified after '#doorpass'")
                self.post_failure()
                return
            
            doorway_name = tokens[1]
            print(f"Attempting to pass through doorway: {doorway_name}")
            super().start(DataEvent(doorway_name))
    
    class CmdPilotToAruco(PilotToPose):
        def start(self, event):
            tokens = event.data.split()
            if len(tokens) < 2:
                print("No marker ID after '#pilottoaruco'")
                self.post_failure()
                return

            arg = tokens[1]
            obj_id = f"ArucoMarker-{arg}.a" if not arg.startswith("ArucoMarker-") else arg
            world_map = self.robot.world_map
            marker = world_map.objects.get(obj_id)
            
            if marker is None or not isinstance(marker, ArucoMarkerObj):
                print(f"No such ArUco marker in world_map: {obj_id}")
                self.post_failure()
                return

            offset_dist = -150 
            heading = self.robot.pose.theta 
            theta = marker.pose.theta
            offset_x = marker.pose.x - offset_dist * math.cos(theta)
            offset_y = marker.pose.y - offset_dist * math.sin(theta)

            offset_pose = Pose(offset_x, offset_y, theta=heading)
            print(f"Piloting to offset pose near ArUco marker {obj_id}: {offset_pose}")
            super().start(DataEvent(offset_pose))

    class WaitThenGotoAruco(StateNode):
        def start(self, event):
            self.saved_data = event.data
            super().start(event)

        def setup(self):
            #             StateNode() =T(0.5)=> pilot
            #             pilot: CmdPilotToAruco()
            
            # Code generated by genfsm on Wed Apr 23 15:14:10 2025:
            
            statenode1 = StateNode() .set_name("statenode1") .set_parent(self)
            pilot = CmdPilotToAruco() .set_name("pilot") .set_parent(self)
            
            timertrans1 = TimerTrans(0.5) .set_name("timertrans1")
            timertrans1 .add_sources(statenode1) .add_destinations(pilot)
            
            return self
    
    class SpeakResponse(Say):
      def start(self,event):
        self.text = event.data
        super().start(event)
        
    def start(self):
        self.robot.openai_client.set_preamble(new_preamble)
        super().start()

    def setup(self):
        #       Say("Welcome to Tepper Museum! I am your personal guide today, what can I help you?") =C=> loop
        # 
        #       loop: StateNode() =Hear()=> AskGPT() =OpenAITrans()=> check
        # 
        #       check: self.CheckResponse()
        #       check =D(list)=> dispatch
        #       check =D(str)=> self.SpeakResponse() =C=> loop
        # 
        #       dispatch: Iterate()
        #       dispatch =D(re.compile('#say '))=> self.CmdSay() =CNext=> dispatch
        #       dispatch =D(re.compile('#forward '))=> self.CmdForward() =CNext=> dispatch
        #       dispatch =D(re.compile('#sideways '))=> self.CmdSideways() =CNext=> dispatch
        #       dispatch =D(re.compile('#turn '))=> self.CmdTurn() =CNext=> dispatch
        #       dispatch =D(re.compile('#turntoward '))=> turntoward
        #       dispatch =D(re.compile('#drop$'))=> self.CmdDrop() =CNext=> dispatch
        #       dispatch =D(re.compile('#pickup '))=> pickup
        #       dispatch =D(re.compile('#glow '))=> self.CmdGlow() =CNext=> dispatch
        #       dispatch =D(re.compile('#doorpass '))=> doorpass  
        #       dispatch =D(re.compile('#pilottoaruco '))=> wait_then_aruco
        #       dispatch =D(re.compile('#camera$'))=> self.CmdSendCamera() =C=>
        #         AskGPT("Please respond to the query using the camera image.") =OpenAITrans()=> check
        #       dispatch =D()=> Print() =Next=> dispatch
        #       dispatch =C=> loop
        # 
        #       turntoward: self.CmdTurnToward()
        #       turntoward =CNext=> dispatch
        #       turntoward =F=> StateNode() =Next=> dispatch
        # 
        #       pickup: self.CmdPickup()
        #       pickup =CNext=> dispatch
        #       pickup =F=> StateNode() =Next=> dispatch
        # 
        #       doorpass: self.CmdDoorPass()
        #       doorpass =CNext=> dispatch
        #       doorpass =F=> Say("Could not pass through that doorway.") =CNext=> dispatch
        # 
        #       wait_then_aruco: self.WaitThenGotoAruco()
        #       wait_then_aruco =CNext=> dispatch
        #       wait_then_aruco =F=> Say("Could not find that marker.") =CNext=> dispatch
        #       wait_then_aruco =PILOT(GoalUnreachable)=> Say("That marker is unreachable.") =CNext=> dispatch
        # 
        # 
        
        # Code generated by genfsm on Wed Apr 23 15:14:10 2025:
        
        say1 = Say("Welcome to Tepper Museum! I am your personal guide today, what can I help you?") .set_name("say1") .set_parent(self)
        loop = StateNode() .set_name("loop") .set_parent(self)
        askgpt1 = AskGPT() .set_name("askgpt1") .set_parent(self)
        check = self.CheckResponse() .set_name("check") .set_parent(self)
        speakresponse1 = self.SpeakResponse() .set_name("speakresponse1") .set_parent(self)
        dispatch = Iterate() .set_name("dispatch") .set_parent(self)
        cmdsay1 = self.CmdSay() .set_name("cmdsay1") .set_parent(self)
        cmdforward1 = self.CmdForward() .set_name("cmdforward1") .set_parent(self)
        cmdsideways1 = self.CmdSideways() .set_name("cmdsideways1") .set_parent(self)
        cmdturn1 = self.CmdTurn() .set_name("cmdturn1") .set_parent(self)
        cmddrop1 = self.CmdDrop() .set_name("cmddrop1") .set_parent(self)
        cmdglow1 = self.CmdGlow() .set_name("cmdglow1") .set_parent(self)
        cmdsendcamera1 = self.CmdSendCamera() .set_name("cmdsendcamera1") .set_parent(self)
        askgpt2 = AskGPT("Please respond to the query using the camera image.") .set_name("askgpt2") .set_parent(self)
        print1 = Print() .set_name("print1") .set_parent(self)
        turntoward = self.CmdTurnToward() .set_name("turntoward") .set_parent(self)
        statenode2 = StateNode() .set_name("statenode2") .set_parent(self)
        pickup = self.CmdPickup() .set_name("pickup") .set_parent(self)
        statenode3 = StateNode() .set_name("statenode3") .set_parent(self)
        doorpass = self.CmdDoorPass() .set_name("doorpass") .set_parent(self)
        say2 = Say("Could not pass through that doorway.") .set_name("say2") .set_parent(self)
        wait_then_aruco = self.WaitThenGotoAruco() .set_name("wait_then_aruco") .set_parent(self)
        say3 = Say("Could not find that marker.") .set_name("say3") .set_parent(self)
        say4 = Say("That marker is unreachable.") .set_name("say4") .set_parent(self)
        
        completiontrans1 = CompletionTrans() .set_name("completiontrans1")
        completiontrans1 .add_sources(say1) .add_destinations(loop)
        
        heartrans1 = HearTrans() .set_name("heartrans1")
        heartrans1 .add_sources(loop) .add_destinations(askgpt1)
        
        openaitrans1 = OpenAITrans() .set_name("openaitrans1")
        openaitrans1 .add_sources(askgpt1) .add_destinations(check)
        
        datatrans1 = DataTrans(list) .set_name("datatrans1")
        datatrans1 .add_sources(check) .add_destinations(dispatch)
        
        datatrans2 = DataTrans(str) .set_name("datatrans2")
        datatrans2 .add_sources(check) .add_destinations(speakresponse1)
        
        completiontrans2 = CompletionTrans() .set_name("completiontrans2")
        completiontrans2 .add_sources(speakresponse1) .add_destinations(loop)
        
        datatrans3 = DataTrans(re.compile('#say ')) .set_name("datatrans3")
        datatrans3 .add_sources(dispatch) .add_destinations(cmdsay1)
        
        cnexttrans1 = CNextTrans() .set_name("cnexttrans1")
        cnexttrans1 .add_sources(cmdsay1) .add_destinations(dispatch)
        
        datatrans4 = DataTrans(re.compile('#forward ')) .set_name("datatrans4")
        datatrans4 .add_sources(dispatch) .add_destinations(cmdforward1)
        
        cnexttrans2 = CNextTrans() .set_name("cnexttrans2")
        cnexttrans2 .add_sources(cmdforward1) .add_destinations(dispatch)
        
        datatrans5 = DataTrans(re.compile('#sideways ')) .set_name("datatrans5")
        datatrans5 .add_sources(dispatch) .add_destinations(cmdsideways1)
        
        cnexttrans3 = CNextTrans() .set_name("cnexttrans3")
        cnexttrans3 .add_sources(cmdsideways1) .add_destinations(dispatch)
        
        datatrans6 = DataTrans(re.compile('#turn ')) .set_name("datatrans6")
        datatrans6 .add_sources(dispatch) .add_destinations(cmdturn1)
        
        cnexttrans4 = CNextTrans() .set_name("cnexttrans4")
        cnexttrans4 .add_sources(cmdturn1) .add_destinations(dispatch)
        
        datatrans7 = DataTrans(re.compile('#turntoward ')) .set_name("datatrans7")
        datatrans7 .add_sources(dispatch) .add_destinations(turntoward)
        
        datatrans8 = DataTrans(re.compile('#drop$')) .set_name("datatrans8")
        datatrans8 .add_sources(dispatch) .add_destinations(cmddrop1)
        
        cnexttrans5 = CNextTrans() .set_name("cnexttrans5")
        cnexttrans5 .add_sources(cmddrop1) .add_destinations(dispatch)
        
        datatrans9 = DataTrans(re.compile('#pickup ')) .set_name("datatrans9")
        datatrans9 .add_sources(dispatch) .add_destinations(pickup)
        
        datatrans10 = DataTrans(re.compile('#glow ')) .set_name("datatrans10")
        datatrans10 .add_sources(dispatch) .add_destinations(cmdglow1)
        
        cnexttrans6 = CNextTrans() .set_name("cnexttrans6")
        cnexttrans6 .add_sources(cmdglow1) .add_destinations(dispatch)
        
        datatrans11 = DataTrans(re.compile('#doorpass ')) .set_name("datatrans11")
        datatrans11 .add_sources(dispatch) .add_destinations(doorpass)
        
        datatrans12 = DataTrans(re.compile('#pilottoaruco ')) .set_name("datatrans12")
        datatrans12 .add_sources(dispatch) .add_destinations(wait_then_aruco)
        
        datatrans13 = DataTrans(re.compile('#camera$')) .set_name("datatrans13")
        datatrans13 .add_sources(dispatch) .add_destinations(cmdsendcamera1)
        
        completiontrans3 = CompletionTrans() .set_name("completiontrans3")
        completiontrans3 .add_sources(cmdsendcamera1) .add_destinations(askgpt2)
        
        openaitrans2 = OpenAITrans() .set_name("openaitrans2")
        openaitrans2 .add_sources(askgpt2) .add_destinations(check)
        
        datatrans14 = DataTrans() .set_name("datatrans14")
        datatrans14 .add_sources(dispatch) .add_destinations(print1)
        
        nexttrans1 = NextTrans() .set_name("nexttrans1")
        nexttrans1 .add_sources(print1) .add_destinations(dispatch)
        
        completiontrans4 = CompletionTrans() .set_name("completiontrans4")
        completiontrans4 .add_sources(dispatch) .add_destinations(loop)
        
        cnexttrans7 = CNextTrans() .set_name("cnexttrans7")
        cnexttrans7 .add_sources(turntoward) .add_destinations(dispatch)
        
        failuretrans1 = FailureTrans() .set_name("failuretrans1")
        failuretrans1 .add_sources(turntoward) .add_destinations(statenode2)
        
        nexttrans2 = NextTrans() .set_name("nexttrans2")
        nexttrans2 .add_sources(statenode2) .add_destinations(dispatch)
        
        cnexttrans8 = CNextTrans() .set_name("cnexttrans8")
        cnexttrans8 .add_sources(pickup) .add_destinations(dispatch)
        
        failuretrans2 = FailureTrans() .set_name("failuretrans2")
        failuretrans2 .add_sources(pickup) .add_destinations(statenode3)
        
        nexttrans3 = NextTrans() .set_name("nexttrans3")
        nexttrans3 .add_sources(statenode3) .add_destinations(dispatch)
        
        cnexttrans9 = CNextTrans() .set_name("cnexttrans9")
        cnexttrans9 .add_sources(doorpass) .add_destinations(dispatch)
        
        failuretrans3 = FailureTrans() .set_name("failuretrans3")
        failuretrans3 .add_sources(doorpass) .add_destinations(say2)
        
        cnexttrans10 = CNextTrans() .set_name("cnexttrans10")
        cnexttrans10 .add_sources(say2) .add_destinations(dispatch)
        
        cnexttrans11 = CNextTrans() .set_name("cnexttrans11")
        cnexttrans11 .add_sources(wait_then_aruco) .add_destinations(dispatch)
        
        failuretrans4 = FailureTrans() .set_name("failuretrans4")
        failuretrans4 .add_sources(wait_then_aruco) .add_destinations(say3)
        
        cnexttrans12 = CNextTrans() .set_name("cnexttrans12")
        cnexttrans12 .add_sources(say3) .add_destinations(dispatch)
        
        pilottrans1 = PilotTrans(GoalUnreachable) .set_name("pilottrans1")
        pilottrans1 .add_sources(wait_then_aruco) .add_destinations(say4)
        
        cnexttrans13 = CNextTrans() .set_name("cnexttrans13")
        cnexttrans13 .add_sources(say4) .add_destinations(dispatch)
        
        return self
