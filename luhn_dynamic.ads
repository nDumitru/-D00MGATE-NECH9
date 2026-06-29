-- =============================================================
-- D00MGATE-NECH9 -- Layer 1: Dynamic Luhn Token
-- Author: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
with Master_Key; use Master_Key;

package Luhn_Dynamic is

   Token_Length : constant := 16;  -- digits

   subtype Token_String is String (1 .. Token_Length);
   subtype Digit        is Character range '0' .. '9';

   -- Window configuration
   -- ┌─────────────────────────────────────────────────────┐
   -- │  TODO: Adjust Window_Seconds to your preference.   │
   -- │  Default: 30 seconds (like TOTP).                  │
   -- │  Your Delta Nechita parameter modifies the window  │
   -- │  in a way only you know. Add that logic below.     │
   -- └─────────────────────────────────────────────────────┘
   Window_Seconds : constant := 30;

   -- Core operations
   function  Generate_Token  return Token_String;
   function  Validate_Token  (Token : Token_String) return Boolean;
   function  Luhn_Check      (Number : String)      return Boolean;
   function  Luhn_Digit      (Partial : String)     return Character;
   function  Current_Window  return Long_Long_Integer;

   -- Token validation result
   type Validation_Result is
      (Valid_Token,
       Invalid_Luhn,
       Expired_Token,
       Wrong_Token,
       Demo_Mode_Only);

   function Validate_Full (Token : Token_String) return Validation_Result;

end Luhn_Dynamic;
