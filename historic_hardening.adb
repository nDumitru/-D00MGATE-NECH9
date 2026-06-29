with Master_Key; use Master_Key;
-- =============================================================
-- D00MGATE-NECH9 -- HistoricHardening Body
-- Author: Dumitru Nechita | Original concept: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
with Ada.Text_IO;    use Ada.Text_IO;
with Ada.Calendar;   use Ada.Calendar;
with GNAT.SHA256;

package body Historic_Hardening is

   Schedule_Interval : constant Duration := 7_776_000.0;  -- 90 days

   function Now return Duration is
   begin
      return Clock - Time_Of (1970, 1, 1, 0.0);
   end Now;

   -- ── Strength multiplier ───────────────────────────────────────
   function Compute_Strength (Breaches    : Natural;
                              Near_Misses : Natural;
                              Novel       : Natural)
                              return Float
   is
      Base : Float := 1.0;
   begin
      Base := Base + Float (Breaches)    * 0.80;
      Base := Base + Float (Near_Misses) * 0.15;
      Base := Base + Float (Novel)       * 0.40;
      if Base > 50.0 then Base := 50.0; end if;
      return Base;
   end Compute_Strength;

   -- ── Initialize ───────────────────────────────────────────────
   procedure Initialize (Engine : out Engine_State) is
   begin
      Engine.Log_Count    := 0;
      Engine.Report_Count := 0;
      Engine.Pending_N    := 0;
      Engine.Layer_Counts := (others => 0);
      Engine.Last_Sched   := Now;
      Put_Line ("[HARDENING] Engine initialized.");
   end Initialize;

   -- ── Record attempt ───────────────────────────────────────────
   procedure Record_Attempt (Engine  : in out Engine_State;
                             Attempt : Attempt_Record)
   is

      Do_Analyze  : Boolean := False;
      Trig        : Trigger := Post_Breach;
      Report      : Hardening_Report;
   begin
      -- Store attempt
      if Engine.Log_Count < Max_Log then
         Engine.Log_Count := Engine.Log_Count + 1;
         Engine.Log (Engine.Log_Count) := Attempt;
         Engine.Log (Engine.Log_Count).Valid := True;
      end if;

      -- Layer count
      if Attempt.Layer_Num in 1 .. Max_Layers then
         Engine.Layer_Counts (Attempt.Layer_Num) :=
            Engine.Layer_Counts (Attempt.Layer_Num) + 1;
      end if;

      -- Check triggers
      if Attempt.Result = Breach then
         Do_Analyze := True;
         Trig       := Post_Breach;
      end if;

      if Engine.Layer_Counts (Attempt.Layer_Num) mod 1000 = 0 then
         Do_Analyze := True;
         Trig       := Threshold;
      end if;

      if Now - Engine.Last_Sched > Schedule_Interval then
         Do_Analyze        := True;
         Trig              := Scheduled;
         Engine.Last_Sched := Now;
      end if;

      if Do_Analyze then
         Report := Generate_Report (Engine, Trig);
         Put_Line ("[HARDENING] Trigger: " & Trigger'Image (Trig) &
                   " | Strength: " & Float'Image (Report.Strength_Delta) & "x");
      end if;
   end Record_Attempt;

   -- ── Generate hardening report ────────────────────────────────
   function Generate_Report (Engine : in out Engine_State;
                             Trig   : Trigger)
                             return Hardening_Report
   is
      Report      : Hardening_Report;
      Breaches    : Natural := 0;
      Near_Misses : Natural := 0;
      Novel       : Natural := 0;
      Id_Seed     : constant String :=
                     Trigger'Image (Trig) & Duration'Image (Now);
      Id_Hash     : constant String := GNAT.SHA256.Digest (Id_Seed);
   begin
      -- Scan all attempts
      for I in 1 .. Engine.Log_Count loop
         if Engine.Log (I).Valid then
            if Engine.Log (I).Result = Breach then
               Breaches := Breaches + 1;
            end if;
            if Engine.Log (I).Partial_Pct >= Near_Miss_Threshold * 100.0 then
               Near_Misses := Near_Misses + 1;
            end if;
            if Engine.Log (I).Attack_Pat = Unknown_Novel then
               Novel := Novel + 1;
            end if;
         end if;
      end loop;

      Report.Report_Id      := Id_Hash (Id_Hash'First ..
                                         Id_Hash'First + 11);
      Report.Timestamp      := Now;
      Report.Trigger_Type   := Trig;
      Report.History_Depth  := Engine.Log_Count;
      Report.Near_Miss_Count:= Near_Misses;
      Report.Novel_Count    := Novel;
      Report.Breach_Count   := Breaches;
      Report.Strength_Delta := Compute_Strength (Breaches, Near_Misses, Novel);
      Report.Pending_Sign   := True;
      Report.Valid          := True;

      if Engine.Report_Count < Max_Reports then
         Engine.Report_Count := Engine.Report_Count + 1;
         Engine.Reports (Engine.Report_Count) := Report;
         Engine.Pending_N := Engine.Pending_N + 1;
      end if;

      Put_Line ("[HARDENING] Report " & Report.Report_Id &
                " | depth:" & Natural'Image (Engine.Log_Count) &
                " | near-miss:" & Natural'Image (Near_Misses) &
                " | delta:" & Float'Image (Report.Strength_Delta) & "x");
      Put_Line ("[HARDENING] Master Key signature required.");

      -- ── TODO: Add your hardening implementation here ──────────
      -- Based on patterns found above, this is where you add
      -- the actual layer modification logic.
      -- What changes in the layers after hardening is YOUR
      -- Delta Nechita parameter in action.
      -- ─────────────────────────────────────────────────────────

      return Report;
   end Generate_Report;

   -- ── Approve report with Master Key ───────────────────────────
   function Approve_Report (Engine    : in out Engine_State;
                            Report_Id : String;
                            Proof     : String)
                            return Boolean
   is
   begin
      if not Require ("Approve_Hardening") then
         return False;
      end if;

      for I in 1 .. Engine.Report_Count loop
         if Engine.Reports (I).Valid
            and Engine.Reports (I).Pending_Sign
            and Engine.Reports (I).Report_Id = Report_Id
         then
            Engine.Reports (I).Pending_Sign := False;
            Engine.Pending_N := Engine.Pending_N - 1;
            Put_Line ("[HARDENING] Report " & Report_Id &
                      " approved. Strength:" &
                      Float'Image (Engine.Reports (I).Strength_Delta) &
                      "x | Signed: Dumitru Nechita");
            return True;
         end if;
      end loop;

      Put_Line ("[HARDENING] Report not found: " & Report_Id);
      return False;
   end Approve_Report;

   -- ── Print summary ────────────────────────────────────────────
   procedure Print_Summary (Engine : Engine_State) is
      Breaches    : Natural := 0;
      Near_Misses : Natural := 0;
      Novel       : Natural := 0;
   begin
      for I in 1 .. Engine.Log_Count loop
         if Engine.Log (I).Valid then
            if Engine.Log (I).Result = Breach then Breaches := Breaches + 1; end if;
            if Engine.Log (I).Partial_Pct >= Near_Miss_Threshold * 100.0 then
               Near_Misses := Near_Misses + 1;
            end if;
            if Engine.Log (I).Attack_Pat = Unknown_Novel then Novel := Novel + 1; end if;
         end if;
      end loop;

      Put_Line ("[HARDENING] Summary:");
      Put_Line ("  Total attempts:  " & Natural'Image (Engine.Log_Count));
      Put_Line ("  Breaches:        " & Natural'Image (Breaches));
      Put_Line ("  Near-misses:     " & Natural'Image (Near_Misses));
      Put_Line ("  Novel vectors:   " & Natural'Image (Novel));
      Put_Line ("  Reports:         " & Natural'Image (Engine.Report_Count));
      Put_Line ("  Pending sign:    " & Natural'Image (Engine.Pending_N));
      Put_Line ("  Strength factor: " &
                Float'Image (Compute_Strength (Breaches, Near_Misses, Novel)) & "x");
      Put_Line ("  'The system gets stronger every time you try.'");
   end Print_Summary;

end Historic_Hardening;
