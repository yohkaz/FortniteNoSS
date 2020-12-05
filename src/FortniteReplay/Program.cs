using System;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Collections.Generic;
using FortniteReplayReader;
using FortniteReplayReader.Models;

namespace FortniteReplay
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var replayPath = args[0];
            var reader = new ReplayReader();
            var replay = reader.ReadReplay(replayPath);
            var players = new List<PlayerData>();
            foreach (PlayerData playerData in replay.PlayerData) {
                if (!String.IsNullOrEmpty(playerData.PlayerId)) {
                    players.Add(playerData);
                }
            }
            var data = new { players = players, killfeed = replay.Eliminations };
            Console.Write(JsonSerializer.Serialize(data));
        }
    }
}
