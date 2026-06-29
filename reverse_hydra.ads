-- =============================================================
-- D00MGATE-NECH9 -- ReverseHydra Evolution Engine
-- Author: Dumitru Nechita | Original concept: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
-- PRINCIPLE:
--   Human break   -> 2 heads spawned
--   AI-Assisted   -> 3 heads spawned
--   Full AI       -> 4 heads (maximum punishment)
--   Team          -> 3 heads
--   Generation N  -> split^N heads (exponential)
--   Layer 9       -> NEVER evolves via competition
-- Master Key signature required for EVERY evolution.
-- "You killed one head. You fed the others."
-- =============================================================
with Master_Key; use Master_Key;

package Reverse_Hydra is

   -- ── Constants ────────────────────────────────────────────────
   Max_Layers     : constant := 10;
   Max_Heads      : constant := 64;   -- cap per layer
   Immutable_Layer: constant := 9;    -- Layer 9 never splits
   Max_Head_Id    : constant := 12;   -- hex chars

   -- ── Break types ──────────────────────────────────────────────
   type Break_Type is
      (Human,
       AI_Assisted,
       Full_AI,       -- Spawns most heads
       Team);

   -- ── Head state ───────────────────────────────────────────────
   type Hydra_State is
      (Stable,
       Broken,
       Pending_Master,  -- Waiting for MK signature
       Multi_Head);

   -- ── Urgency for master notification ──────────────────────────
   type Urgency_Level is
      (Info,       --  0-1 hour
       Warning,    --  1-6 hours
       Urgent,     --  6-24 hours
       Critical);  -- 24h+ layer offline

   -- ── Head record ──────────────────────────────────────────────
   subtype Head_Id_String  is String (1 .. Max_Head_Id);
   subtype Version_String  is String (1 .. 16);

   type Hydra_Head is record
      Head_Id    : Head_Id_String  := (others => '0');
      Version    : Version_String  := (others => ' ');
      Layer_Num  : Positive        := 1;
      Generation : Positive        := 1;
      Active     : Boolean         := True;
      Created_At : Duration        := 0.0;
   end record;

   type Head_Array is array (1 .. Max_Heads) of Hydra_Head;

   -- ── Layer state record ────────────────────────────────────────
   type Layer_State is record
      State      : Hydra_State := Stable;
      Head_Count : Natural     := 1;
      Heads      : Head_Array;
      Breaks     : Natural     := 0;
   end record;

   -- ── Notification record ───────────────────────────────────────
   subtype Notif_Id_String is String (1 .. 16);

   type Master_Notification is record
      Notif_Id   : Notif_Id_String := (others => '0');
      Layer_Num  : Positive        := 1;
      Heads_N    : Positive        := 2;
      Created_At : Duration        := 0.0;
      Urgency    : Urgency_Level   := Info;
      Acked      : Boolean         := False;
   end record;

   -- ── Attack vector ─────────────────────────────────────────────
   type Attack_Vector is record
      Layer_Num       : Positive   := 1;
      Attack_Type     : Break_Type := Human;
      Competitor_Id   : String (1 .. 32) := (others => ' ');
      Attempts        : Natural    := 0;
      AI_Probability  : Float      := 0.0;
      Version_Broken  : Version_String := (others => ' ');
      Pattern         : String (1 .. 32) := (others => ' ');
      Replication_Risk: Float      := 0.0;
   end record;

   -- ── Process result ───────────────────────────────────────────
   type Process_Result is
      (Pending_Master_Sig,
       Layer_9_Immutable,
       Evolution_Complete,
       Error_Not_Found);

   -- ── Engine state (global) ─────────────────────────────────────
   type Engine_State is limited private;

   -- ── Main operations ──────────────────────────────────────────

   procedure Initialize    (Engine : out Engine_State);

   function  Process_Break (Engine : in out Engine_State;
                            Attack : Attack_Vector)
                            return Process_Result;

   function  Master_Acknowledge
                           (Engine   : in out Engine_State;
                            Notif_Id : Notif_Id_String;
                            Proof    : String)
                            return Process_Result;

   procedure Check_Notifications
                           (Engine : in out Engine_State);

   procedure Print_Status  (Engine : Engine_State;
                            Layer  : Positive := 0);

   -- ── Split count by type ──────────────────────────────────────
   function Split_Count (BT : Break_Type) return Positive;

private

   Max_Pending : constant := 32;

   type Pending_Array    is array (1 .. Max_Pending) of Master_Notification;
   type Layer_State_Array is array (1 .. Max_Layers)  of Layer_State;

   type Engine_State is limited record
      Layers      : Layer_State_Array;
      Pending     : Pending_Array;
      Pending_N   : Natural  := 0;
      Total_Evols : Natural  := 0;
   end record;

end Reverse_Hydra;
