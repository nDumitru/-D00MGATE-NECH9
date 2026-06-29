-- =============================================================
-- D00MGATE-NECH9 -- HistoricHardening Engine Specification
-- Author: Dumitru Nechita | Original concept: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
-- Analyzes ALL past attempts across ALL layers -> cumulative
-- hardening. Near-misses (>75%) weighted MORE than breaches.
-- Cross-layer pattern detection included.
-- "The system does not forget. It gets stronger every time."
-- =============================================================

package Historic_Hardening is

   Max_Log     : constant := 1000;  -- max attempts stored
   Max_Reports : constant := 100;
   Max_Layers  : constant := 10;

   Near_Miss_Threshold : constant Float := 0.75;  -- 75% completion

   -- ── Attack outcome ───────────────────────────────────────────
   type Outcome is
      (Failed_Early,
       Failed_Mid,
       Failed_Late,
       Breach,
       Partial);

   -- ── Attack pattern classification ────────────────────────────
   type Pattern is
      (Timing_Attack,
       Bruteforce,
       ML_Enumeration,
       Side_Channel,
       Hybrid_Coordinated,
       Unknown_Novel);   -- Most dangerous, highest hardening value

   -- ── What triggered the hardening analysis ────────────────────
   type Trigger is
      (Post_Breach,
       Threshold,    -- After 1000 attempts on one layer
       Scheduled,    -- Every 90 days
       Cross_Layer,  -- Same pattern seen on 3+ layers
       Manual);      -- Master Key holder decides

   -- ── Single attempt record ─────────────────────────────────────
   type Attempt_Record is record
      Attempt_Id   : String (1 .. 8)  := (others => '0');
      Layer_Num    : Positive          := 1;
      Timestamp    : Duration          := 0.0;
      Result       : Outcome           := Failed_Early;
      Attacker     : String (1 .. 16)  := (others => ' ');
      AI_Prob      : Float             := 0.0;
      Attack_Pat   : Pattern           := Bruteforce;
      Partial_Pct  : Float             := 0.0;  -- 0.0 to 100.0
      Attempt_Count: Natural           := 0;
      Valid        : Boolean           := False;
   end record;

   -- ── Hardening report ─────────────────────────────────────────
   type Hardening_Report is record
      Report_Id      : String (1 .. 12) := (others => '0');
      Timestamp      : Duration         := 0.0;
      Trigger_Type   : Trigger          := Post_Breach;
      History_Depth  : Natural          := 0;
      Near_Miss_Count: Natural          := 0;
      Novel_Count    : Natural          := 0;
      Breach_Count   : Natural          := 0;
      Strength_Delta : Float            := 1.0;  -- multiplier
      Pending_Sign   : Boolean          := True;
      Valid          : Boolean          := False;
   end record;

   -- ── Engine state ─────────────────────────────────────────────
   type Engine_State is limited private;

   -- ── Main operations ──────────────────────────────────────────
   procedure Initialize   (Engine : out Engine_State);

   procedure Record_Attempt (Engine  : in out Engine_State;
                             Attempt : Attempt_Record);

   function  Generate_Report (Engine  : in out Engine_State;
                              Trig    : Trigger)
                              return Hardening_Report;

   function  Approve_Report  (Engine    : in out Engine_State;
                              Report_Id : String;
                              Proof     : String)
                              return Boolean;

   procedure Print_Summary   (Engine : Engine_State);

   -- ── Strength calculation (public formula) ────────────────────
   function  Compute_Strength (Breaches   : Natural;
                               Near_Misses: Natural;
                               Novel      : Natural)
                               return Float;

private

   type Log_Array    is array (1 .. Max_Log)     of Attempt_Record;
   type Report_Array is array (1 .. Max_Reports) of Hardening_Report;
   type Count_Array  is array (1 .. Max_Layers)  of Natural;

   type Engine_State is limited record
      Log          : Log_Array;
      Log_Count    : Natural       := 0;
      Reports      : Report_Array;
      Report_Count : Natural       := 0;
      Pending_N    : Natural       := 0;
      Layer_Counts : Count_Array   := (others => 0);
      Last_Sched   : Duration      := 0.0;
   end record;

end Historic_Hardening;
