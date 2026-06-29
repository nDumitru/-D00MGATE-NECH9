-- =============================================================
-- D00MGATE-NECH9 -- Main Demo Program
-- Author: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
-- Compile:  gnatmake -P doomgate.gpr
-- Run:      ./build/doomgate_demo
-- =============================================================
with Ada.Text_IO;        use Ada.Text_IO;
with Master_Key;
with Luhn_Dynamic;       use Luhn_Dynamic;
with Reverse_Hydra;      use Reverse_Hydra;
with Historic_Hardening; use Historic_Hardening;
with Veridex;            use Veridex;

procedure Doomgate_Demo is

   Border : constant String (1 .. 56) := (others => '=');

   -- ── DEMO: Luhn Dynamic (Layer 1) ─────────────────────────────
   procedure Demo_Luhn is
      Token  : Token_String;
      Result : Validation_Result;
   begin
      Put_Line (Border);
      Put_Line ("  LAYER 1 -- Dynamic Luhn Token Demo");
      Put_Line (Border);

      Token := Generate_Token;
      Put_Line ("[LUHN] Generated token: " & Token);
      Put_Line ("[LUHN] Window:" & Long_Long_Integer'Image (Current_Window));

      Result := Validate_Full (Token);
      Put_Line ("[LUHN] Self-validation: " & Validation_Result'Image (Result));

      -- Test with wrong token
      declare
         Wrong : Token_String := Token;
      begin
         Wrong (Wrong'Last) :=
            (if Wrong (Wrong'Last) = '9' then '0' else
             Character'Val (Character'Pos (Wrong (Wrong'Last)) + 1));
         Result := Validate_Full (Wrong);
         Put_Line ("[LUHN] Wrong token result: " &
                   Validation_Result'Image (Result));
      end;

      -- Luhn check on known valid number
      Put_Line ("[LUHN] Known valid (4539148803436467): " &
                Boolean'Image (Luhn_Check ("4539148803436467")));
      Put_Line ("[LUHN] Known invalid (1234567890123456): " &
                Boolean'Image (Luhn_Check ("1234567890123456")));
      New_Line;
   end Demo_Luhn;

   -- ── DEMO: ReverseHydra ───────────────────────────────────────
   procedure Demo_Hydra is
      Engine : Reverse_Hydra.Engine_State;
      Attack : Attack_Vector;
      Result : Process_Result;
      -- Notif_Id_String not needed in this demo
   begin
      Put_Line (Border);
      Put_Line ("  REVERSHYDRA ENGINE Demo");
      Put_Line ("  Original concept: Dumitru Nechita");
      Put_Line (Border);

      Initialize (Engine);

      -- AI breaks Layer 1 (-> 4 heads)
      Attack.Layer_Num     := 1;
      Attack.Attack_Type   := Full_AI;
      Attack.Competitor_Id := (others => ' ');
      Attack.Competitor_Id (1 .. 8) := "AI_DEMO_";
      Attack.Attempts      := 50000;
      Attack.AI_Probability:= 0.97;
      Attack.Version_Broken:= (others => ' ');
      Attack.Version_Broken (1 .. 3) := "1.0";

      declare R1 : constant Process_Result := Process_Break (Engine, Attack); begin
         Put_Line ("[HYDRA] Process result: " & Process_Result'Image (R1));
      end;

      -- Simulate master acknowledge (demo - no real key)
      -- Note: In production, Notif_Id comes from Process_Break return value
      -- For demo we skip ack (Engine internals are private/limited)
      Put_Line ("[HYDRA] Master ack skipped in demo (Engine is limited private).");
      Put_Line ("[HYDRA] In production: call Master_Acknowledge with notif_id");

      -- Human breaks Layer 2 (-> 2 heads)
      Attack.Layer_Num     := 2;
      Attack.Attack_Type   := Human;
      Attack.Attempts      := 843;
      Attack.AI_Probability:= 0.04;

      declare R2 : constant Process_Result := Process_Break (Engine, Attack);
      begin Put_Line ("[HYDRA] Human break: " & Process_Result'Image (R2)); end;

      -- Check notifications
      Check_Notifications (Engine);

      -- Print status
      Print_Status (Engine, 1);
      Print_Status (Engine, 2);

      -- Layer 9 attempt (immutable)
      Attack.Layer_Num   := 9;
      Attack.Attack_Type := Human;
      Result := Process_Break (Engine, Attack);
      Put_Line ("[HYDRA] Layer 9 result: " & Process_Result'Image (Result));

      New_Line;
   end Demo_Hydra;

   -- ── DEMO: HistoricHardening ───────────────────────────────────
   procedure Demo_Hardening is
      Engine  : Historic_Hardening.Engine_State;
      Attempt : Attempt_Record;
      -- Report stored internally by engine
   begin
      Put_Line (Border);
      Put_Line ("  HISTORIC HARDENING ENGINE Demo");
      Put_Line ("  Original concept: Dumitru Nechita");
      Put_Line (Border);

      Initialize (Engine);

      -- Record several attempts
      Attempt.Layer_Num  := 1;
      Attempt.Result     := Failed_Late;
      Attempt.Attack_Pat := ML_Enumeration;
      Attempt.Partial_Pct:= 78.0;
      Attempt.AI_Prob    := 0.95;
      Attempt.Attempt_Count := 50000;
      Attempt.Valid      := True;
      Attempt.Attempt_Id := "A1000001";
      Record_Attempt (Engine, Attempt);

      Attempt.Layer_Num  := 2;
      Attempt.Result     := Breach;
      Attempt.Attack_Pat := Hybrid_Coordinated;
      Attempt.Partial_Pct:= 100.0;
      Attempt.Attempt_Id := "A1000002";
      Record_Attempt (Engine, Attempt);

      Attempt.Layer_Num  := 1;
      Attempt.Result     := Breach;
      Attempt.Attack_Pat := Unknown_Novel;
      Attempt.Partial_Pct:= 100.0;
      Attempt.AI_Prob    := 0.08;
      Attempt.Attempt_Id := "A1000003";
      Record_Attempt (Engine, Attempt);

      Attempt.Layer_Num  := 4;
      Attempt.Result     := Failed_Late;
      Attempt.Attack_Pat := Side_Channel;
      Attempt.Partial_Pct:= 88.0;
      Attempt.Attempt_Id := "A1000004";
      Record_Attempt (Engine, Attempt);

      Print_Summary (Engine);
      New_Line;
   end Demo_Hardening;

   -- ── DEMO: VERIDEX Layer 10 ────────────────────────────────────
   procedure Demo_Veridex is
      State : Veridex_State;
      Token : Component_Token;
      TLKey : Time_Lock_Key;
      pragma Warnings (Off);
   begin
      Put_Line (Border);
      Put_Line ("  VERIDEX Layer 10 Demo");
      Put_Line ("  Original concept: Dumitru Nechita");
      Put_Line ("  'Veritas non moritur.'");
      Put_Line (Border);

      -- P1: Weeping Angel
      Put_Line ("-- P1: ACTIVE INVISIBILITY --");
      Angel_Register (State, "veridex_core", Token);

      -- Unknown observer -> freeze
      declare
         Unknown_Ok : constant Boolean :=
            Angel_Access (State, Token, "UNKNOWN_OBSERVER_000");
      begin
         Put_Line ("[ANGEL] Unknown result: " & Boolean'Image (Unknown_Ok));
      end;

      -- Known observer -> active
      declare
         Known_Prefix : constant String :=
            (if Master_Key.Is_Ready
             then Master_Key.Sign (Token) (1 .. 8)
             else "DEMO_KNO");
         Known_Ok : constant Boolean :=
            Angel_Access (State, Token, Known_Prefix & "_rest");
      begin
         Put_Line ("[ANGEL] Known result: " & Boolean'Image (Known_Ok));
      end;

      -- Silence
      Silence_Execute (State, "key_derivation_op");

      -- P2: TimeLock
      New_Line;
      Put_Line ("-- P2: ASYMMETRIC TEMPORALITY --");
      TLKey := TimeLock_Generate (State, 10);
      if TLKey.Valid then
         Put_Line ("[TIMELOCK] Validate: " &
                   Boolean'Image (TimeLock_Validate (TLKey, 10)));
      end if;

      -- P3: Biological
      New_Line;
      Put_Line ("-- P3: BIOLOGICAL MATTER --");
      Silence_Execute (State, "epigenetic_derive");  -- silent in demo
         declare Dummy : Positive := JunkDNA_Encode ("VERIDEX_PAYLOAD_TEST", 999); begin null; end;

      -- P4: Survival
      New_Line;
      Put_Line ("-- P4: ABSORPTION + SURVIVAL --");
      Gravemind_Absorb (State, "ml_timing_correlation",
                        "full_ai", 0.90);

      declare
         Sealed : constant Boolean := Ark_Seal (State, "DEMO_PROOF");
      begin
         Put_Line ("[ARK] Seal result: " & Boolean'Image (Sealed));
      end;

      declare
         Cont : constant Boolean :=
            Regen_Continuity (State, "9.0.0", "10.1.0", "DEMO");
      begin
         Put_Line ("[REGEN] Continuity: " & Boolean'Image (Cont));
      end;

      -- Status
      New_Line;
      Print_Status (State);
      New_Line;
   end Demo_Veridex;

-- ── MAIN ──────────────────────────────────────────────────────
begin
   Put_Line (Border);
   Put_Line ("  D00MGATE-NECH9 -- Ada Implementation Demo");
   Put_Line ("  Author: Dumitru Nechita | v1.0.0 | 2026");
   Put_Line (Border);

   if not Master_Key.Is_Ready then
      Master_Key.Warn ("main");
      Put_Line ("  Running in DEMO MODE.");
      Put_Line ("  Edit core/master_key.adb to activate.");
   else
      Put_Line ("  Master Key: SET [OK]");
   end if;
   New_Line;

   -- Run all demos
   Demo_Luhn;
   Demo_Hydra;
   Demo_Hardening;
   Demo_Veridex;

   Put_Line (Border);
   Put_Line ("  D00MGATE-NECH9 Demo Complete.");
   Put_Line ("  'The gate is open. The address is mine.'");
   Put_Line ("  -- Dumitru Nechita, 2026");
   Put_Line (Border);

end Doomgate_Demo;
