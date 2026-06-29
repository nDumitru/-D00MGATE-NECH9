-- =============================================================
-- D00MGATE-NECH9 -- ReverseHydra Body
-- Author: Dumitru Nechita | Original concept: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
with Ada.Text_IO;        use Ada.Text_IO;
with Ada.Calendar;       use Ada.Calendar;
with Ada.Strings.Fixed;  use Ada.Strings.Fixed;
with GNAT.SHA256;
with Master_Key;         use Master_Key;

package body Reverse_Hydra is

   Border : constant String (1 .. 52) := (others => '=');

   -- ── Greek suffixes for head versions ─────────────────────────
   type Greek_Array is array (1 .. 16) of String (1 .. 2);
   Greek : constant Greek_Array :=
      ("a ", "b ", "g ", "d ", "e ", "z ", "h ", "th",
       "i ", "k ", "l ", "m ", "n ", "x ", "o ", "p ");

   -- ── Seconds since a fixed epoch (simplified) ─────────────────
   function Now return Duration is
   begin
      return Clock - Time_Of (1970, 1, 1, 0.0);
   end Now;

   -- ── Generate a short hex ID ──────────────────────────────────
   function Make_Id (Seed : String) return Head_Id_String is
      Full : constant String :=
         GNAT.SHA256.Digest (Seed & Duration'Image (Now));
      Result : Head_Id_String;
   begin
      Result := Full (Full'First .. Full'First + Max_Head_Id - 1);
      return Result;
   end Make_Id;

   -- ── Split count ──────────────────────────────────────────────
   function Split_Count (BT : Break_Type) return Positive is
   begin
      case BT is
         when Human       => return 2;
         when AI_Assisted => return 3;
         when Full_AI     => return 4;  -- Most aggressive
         when Team        => return 3;
      end case;
   end Split_Count;

   -- ── Initialize engine ────────────────────────────────────────
   procedure Initialize (Engine : out Engine_State) is
      Genesis_Head : Hydra_Head;
      Ver          : Version_String := (others => ' ');
   begin
      Ver (1 .. 3) := "1.0";
      for L in 1 .. Max_Layers loop
         Engine.Layers (L).State      := Stable;
         Engine.Layers (L).Head_Count := 1;
         Engine.Layers (L).Breaks     := 0;
         Genesis_Head.Head_Id    :=
            Make_Id ("GENESIS_L" & Positive'Image (L));
         Genesis_Head.Version    := Ver;
         Genesis_Head.Layer_Num  := L;
         Genesis_Head.Generation := 1;
         Genesis_Head.Active     := True;
         Genesis_Head.Created_At := Now;
         Engine.Layers (L).Heads (1) := Genesis_Head;
      end loop;
      Engine.Pending_N   := 0;
      Engine.Total_Evols := 0;
      Put_Line ("[HYDRA] Engine initialized. All layers stable.");
   end Initialize;

   -- ── Find active head matching version ────────────────────────
   function Find_Head (Layer   : Layer_State;
                       Version : Version_String)
                       return Natural
   is
   begin
      for I in 1 .. Layer.Head_Count loop
         if Layer.Heads (I).Version = Version
            and Layer.Heads (I).Active
         then
            return I;
         end if;
      end loop;
      return 0;
   end Find_Head;

   -- ── Create notification ───────────────────────────────────────
   function Make_Notification (Layer_Num : Positive;
                               Heads_N   : Positive)
                               return Master_Notification
   is
      N : Master_Notification;
   begin
      declare
         Raw : constant String := Make_Id ("NOTIF_L" & Positive'Image (Layer_Num));
      begin
         N.Notif_Id := (others => '0');
         N.Notif_Id (1 .. Raw'Length) := Raw;
      end;
      N.Layer_Num  := Layer_Num;
      N.Heads_N    := Heads_N;
      N.Created_At := Now;
      N.Urgency    := Info;
      N.Acked      := False;
      return N;
   end Make_Notification;

   -- ── Escalate urgency based on time ───────────────────────────
   procedure Escalate (N : in out Master_Notification) is
      Elapsed : constant Duration := Now - N.Created_At;
   begin
      if    Elapsed > 86400.0 then N.Urgency := Critical;
      elsif Elapsed > 21600.0 then N.Urgency := Urgent;
      elsif Elapsed >  3600.0 then N.Urgency := Warning;
      else                         N.Urgency := Info;
      end if;
   end Escalate;

   -- ── Process a break event ────────────────────────────────────
   function Process_Break (Engine : in out Engine_State;
                           Attack : Attack_Vector)
                           return Process_Result
   is
      Layer_Num : constant Positive := Attack.Layer_Num;
      BT        : constant Break_Type := Attack.Attack_Type;
      N         : Positive := Split_Count (BT);
      Head_Idx  : Natural;
      Gen       : Positive;
      Notif     : Master_Notification;
   begin
      -- ── Layer 9: NEVER splits ────────────────────────────────
      if Layer_Num = Immutable_Layer then
         Put_Line (Border);
         Put_Line ("  [HYDRA] Layer 9 break claimed.");
         Put_Line ("  [HYDRA] Layer 9 is IMMUTABLE.");
         Put_Line ("  [HYDRA] This event is impossible by design.");
         Put_Line ("  [HYDRA] Master notified with CRITICAL urgency.");
         Put_Line (Border);
         return Layer_9_Immutable;
      end if;

      -- ── Find broken head ─────────────────────────────────────
      Head_Idx := Find_Head (Engine.Layers (Layer_Num),
                              Attack.Version_Broken);
      if Head_Idx > 0 then
         Gen := Engine.Layers (Layer_Num).Heads (Head_Idx).Generation;
         Engine.Layers (Layer_Num).Heads (Head_Idx).Active := False;

         -- Exponential for child heads
         if Gen > 1 then
            if Gen <= 2 then N := N * N;
            elsif Gen <= 3 then N := N * N * N; end if;
            if N > Max_Heads then N := Max_Heads; end if;
            Put_Line ("[HYDRA] Gen-" & Positive'Image (Gen) &
                      " head broken -> exponential split:" &
                      Positive'Image (N));
         end if;
      end if;

      -- ── Update state ─────────────────────────────────────────
      Engine.Layers (Layer_Num).State  := Pending_Master;
      Engine.Layers (Layer_Num).Breaks :=
         Engine.Layers (Layer_Num).Breaks + 1;

      -- ── Create notification ───────────────────────────────────
      Notif := Make_Notification (Layer_Num, N);
      if Engine.Pending_N < Max_Pending then
         Engine.Pending_N := Engine.Pending_N + 1;
         Engine.Pending (Engine.Pending_N) := Notif;
      end if;

      -- ── Print report ─────────────────────────────────────────
      Put_Line (Border);
      Put_Line ("  REVERSHYDRA TRIGGERED - Layer" &
                Positive'Image (Layer_Num));
      Put_Line ("  Type: " & Break_Type'Image (BT));
      Put_Line ("  Heads spawning:" & Positive'Image (N));
      Put_Line ("  State: OFFLINE - PENDING MASTER SIGNATURE");
      Put_Line ("  Notification: " & Notif.Notif_Id (1 .. 8) & "...");
      Put_Line ("  Evolution content: REDACTED");
      Put_Line (Border);

      return Pending_Master_Sig;
   end Process_Break;

   -- ── Master acknowledgment ────────────────────────────────────
   function Master_Acknowledge (Engine   : in out Engine_State;
                                Notif_Id : Notif_Id_String;
                                Proof    : String)
                                return Process_Result
   is
      Notif_Idx  : Natural := 0;
      Layer_Num  : Positive;
      Heads_N    : Positive;
      New_Head   : Hydra_Head;
      Ver_Base   : String (1 .. 4);
      New_Ver    : Version_String;
   begin
      -- Require Master Key
      if not Require ("Master_Acknowledge") then
         return Error_Not_Found;
      end if;

      -- ── Find notification ─────────────────────────────────────
      for I in 1 .. Engine.Pending_N loop
         if Engine.Pending (I).Notif_Id = Notif_Id
            and not Engine.Pending (I).Acked
         then
            Notif_Idx := I;
            exit;
         end if;
      end loop;

      if Notif_Idx = 0 then
         Put_Line ("[HYDRA] Notification not found.");
         return Error_Not_Found;
      end if;

      Layer_Num := Engine.Pending (Notif_Idx).Layer_Num;
      Heads_N   := Engine.Pending (Notif_Idx).Heads_N;
      Engine.Pending (Notif_Idx).Acked := True;

      -- ── Spawn new heads ──────────────────────────────────────
      for I in 1 .. Heads_N loop
         exit when Engine.Layers (Layer_Num).Head_Count >= Max_Heads;

         Ver_Base := "2.0-";
         New_Ver  := (others => ' ');
         New_Ver (1 .. 4) := Ver_Base;
         New_Ver (5 .. 6) := Greek (((I - 1) mod 16) + 1);

         New_Head.Head_Id    :=
            Make_Id ("SPLIT_L" & Positive'Image (Layer_Num) &
                     "_" & Positive'Image (I));
         New_Head.Version    := New_Ver;
         New_Head.Layer_Num  := Layer_Num;
         New_Head.Generation := 2;
         New_Head.Active     := True;
         New_Head.Created_At := Now;

         Engine.Layers (Layer_Num).Head_Count :=
            Engine.Layers (Layer_Num).Head_Count + 1;
         Engine.Layers (Layer_Num).Heads
            (Engine.Layers (Layer_Num).Head_Count) := New_Head;
      end loop;

      Engine.Layers (Layer_Num).State  := Multi_Head;
      Engine.Total_Evols := Engine.Total_Evols + 1;

      Put_Line ("[HYDRA] Evolution complete - Layer" &
                Positive'Image (Layer_Num) & ":" &
                Positive'Image (Heads_N) & " new heads active.");
      Put_Line ("[HYDRA] Signed by: Dumitru Nechita - Master Key");
      Put_Line ("[HYDRA] Evolution content: REDACTED");

      -- ── TODO: Add your Delta Nechita evolution logic here ─────
      -- The actual content change to the layer (what attackers
      -- will face in the new heads) is implemented here.
      -- This is the part only YOU know.
      -- ─────────────────────────────────────────────────────────

      return Evolution_Complete;
   end Master_Acknowledge;

   -- ── Check and escalate pending notifications ─────────────────
   procedure Check_Notifications (Engine : in out Engine_State) is
   begin
      if Engine.Pending_N = 0 then
         Put_Line ("[HYDRA] No pending notifications.");
         return;
      end if;

      for I in 1 .. Engine.Pending_N loop
         if not Engine.Pending (I).Acked then
            Escalate (Engine.Pending (I));
            Put_Line ("[HYDRA] Pending L" &
                      Positive'Image (Engine.Pending (I).Layer_Num) &
                      " | " & Urgency_Level'Image (Engine.Pending (I).Urgency) &
                      " | heads waiting:" &
                      Positive'Image (Engine.Pending (I).Heads_N));
            if Engine.Pending (I).Urgency = Critical then
               Put_Line ("  [CRITICAL] Layer" &
                         Positive'Image (Engine.Pending (I).Layer_Num) &
                         " OFFLINE 24h+. Sign immediately.");
            end if;
         end if;
      end loop;
   end Check_Notifications;

   -- ── Print layer status ────────────────────────────────────────
   procedure Print_Status (Engine : Engine_State; Layer : Positive := 0) is
      procedure Print_Layer (L : Positive) is
         LS : constant Layer_State := Engine.Layers (L);
      begin
         Put_Line ("  Layer" & Positive'Image (L) &
                   ": " & Hydra_State'Image (LS.State) &
                   " | heads:" & Natural'Image (LS.Head_Count) &
                   " | breaks:" & Natural'Image (LS.Breaks));
         if LS.State = Multi_Head then
            for I in 1 .. LS.Head_Count loop
               if LS.Heads (I).Active then
                  Put_Line ("    -> " &
                            Trim (LS.Heads (I).Version, Ada.Strings.Right));
               end if;
            end loop;
         end if;
      end Print_Layer;
   begin
      Put_Line ("[HYDRA] Engine Status | Evolutions:" &
                Natural'Image (Engine.Total_Evols));
      if Layer = 0 then
         for L in 1 .. Max_Layers loop
            Print_Layer (L);
         end loop;
      else
         Print_Layer (Layer);
      end if;
   end Print_Status;

end Reverse_Hydra;
