using System;
using System.Dynamic;
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
            foreach (PlayerData playerData in replay.PlayerData) {
                if (!String.IsNullOrEmpty(playerData.PlayerId)) {
                    Console.Write(playerData.PlayerId);
                    Console.Write(',');
                }
            }
        }
    }
}
