import unrealsdk
from unrealsdk import *
import sys
import random
import json
import os

from ..ModManager import BL2MOD, RegisterMod
from Mods.ModMenu import Game, Hook


class CrossSkillModifier(BL2MOD):
    Name: str = "Cross Class Skill Modifier"
    Description: str = "Modify all the skills!"
    Version: str = "1.0"
    # Fork of Cross Class Skill Randomizer 1.2 - https://github.com/bl-sdk/PythonSDK/blob/master/Mods/SkillRandomizer/__init__.py
    Author: str = "Cal"
    # Special thanks to Abahbob + Others for doing a large ammount of heavy lifting!
    SupportedGames = Game.BL2
    LocalModDir: str = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        return

    @Hook("WillowGame.PlayerSkillTree.Initialize")
    def InjectSkills(self, caller: UObject, function: UFunction, params: FStruct) -> bool:
        self.GenerateTrees(params.SkillTreeDef)
        return True

    def PreloadPackages(self) -> None:
        packages = [
            "GD_Assassin_Streaming_SF",
            "GD_Mercenary_Streaming_SF",
            "GD_Siren_Streaming_SF",
            "GD_Lilac_Psycho_Streaming_SF",
            "GD_Tulip_Mechro_Streaming_SF",
            "GD_Soldier_Streaming_SF",
        ]

        for package in packages:
            unrealsdk.LoadPackage(package)

    def GenerateTrees(self, SkillTreeDef) -> None:
        iteration = -1
        for Branch in SkillTreeDef.Root.Children:
            iteration +=1
            self.DefineTree(Branch, iteration)

    def DefineTree(self, SkillTreeBranchDef, iteration) -> None:
        self.PreloadPackages()
        #### Modify here

        # What I am currently playing w/ siren
        Tree_0 = [
            [["GD_Siren_Skills.Cataclysm.Backdraft", False, "GD_Siren_Skills.Motion.Accelerate"], ["GD_Siren_Skills.Motion.Suspension", False, "GD_Siren_Skills.Cataclysm.ChainReaction"], ["GD_Soldier_Skills.Guerrilla.Onslaught", "GD_Siren_Skills.Motion.Converge", "GD_Assassin_Skills.Bloodshed.LikeTheWind"], [False, "GD_Siren_Skills.Motion.Quicken", False], ["GD_Tulip_Mechromancer_Skills.BestFriendsForever.CloseEnough", "GD_Siren_Skills.Motion.SubSequence", False], [False, "GD_Siren_Skills.Cataclysm.Ruin", False]],
            [["GD_Siren_Skills.Harmony.MindsEye", False, "GD_Siren_Skills.Harmony.Wreck"], ["GD_Assassin_Skills.Cunning.Fearless", False, "GD_Lilac_Skills_Hellborn.Skills.NumbedNerves"], ["GD_Soldier_Skills.Survival.HealthY", "GD_Siren_Skills.Harmony.Res", "GD_Lilac_Skills_Hellborn.Skills.ElementalEmpathy"], [False, "GD_Soldier_Skills.Guerrilla.Able", "GD_Lilac_Skills_Hellborn.Skills.FlameFlare"], [False, "GD_Soldier_Skills.Survival.Grit", False], [False, "GD_Siren_Skills.Harmony.Scorn", False]],
            [["GD_Assassin_Skills.Sniping.HeadShot", False, "GD_Mercenary_Skills.Rampage.Inconceivable"], ["GD_Lilac_Skills_Hellborn.Skills.BurnBabyBurn", False, "GD_Lilac_Skills_Hellborn.Skills.FuelTheFire"], ["GD_Siren_Skills.Cataclysm.Flicker", "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.ElectricalBurn", "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.MorePep"], [False, "GD_Siren_Skills.Cataclysm.Reaper", "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.EvilEnchantress"], [False, "GD_Assassin_Skills.Sniping.Killer", False], [False, "GD_Siren_Skills.Cataclysm.CloudKill", False]]
        ]
        # Empty Tree
        Tree_1 = [[[False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False]],  # Branch 1 - e.g. (Maya - Motion)
                  [[False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False]],  # Branch 2 - e.g. (Maya - Harmony)
                  [[False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False], [False, False, False]]  # Branch 3 - e.g. (Maya - Cataclysm)
                  ]


        CurrentTree = Tree_0[iteration] # Modify this if you want to use a different Skill Tree e.g. CurrentTree = Tree_1[iteration]

        #### End Modification

        HasBloodlust = False
        HasHellborn = False
        for Tier in range(6):
            CurrentTier = CurrentTree[Tier]
            NewSkills = []
            MaxPoints = 0
            for Skill in range(3):
                CurrentSkill = CurrentTier[Skill]
                if CurrentSkill != False:
                    SkillDef = unrealsdk.FindObject("SkillDefinition", CurrentSkill)
                    MaxPoints += SkillDef.MaxGrade
                    NewSkills.append(SkillDef)
                    HasHellborn = HasHellborn or "Hellborn" in SkillDef.GetFullName()
                    if not HasBloodlust and SkillDef.GetName() in ["BloodfilledGuns", "BloodyTwitch"]:
                        HasBloodlust = True

            if HasBloodlust:
                NewSkills.append(unrealsdk.FindObject("SkillDefinition", "GD_Lilac_Skills_Bloodlust.Skills._Bloodlust"))
            if HasHellborn:
                NewSkills.append(
                    unrealsdk.FindObject(
                    "SkillDefinition",
                    "GD_Lilac_Skills_Hellborn.Skills.FireStatusDetector",
                    )
                )
                NewSkills.append(
                    unrealsdk.FindObject(
                    "SkillDefinition",
                    "GD_Lilac_Skills_Hellborn.Skills.AppliedStatusEffectListener",
                    )
                )

            bool_array = [bool(value) for value in CurrentTier]
            SkillTreeBranchDef.Layout.Tiers[Tier].bCellIsOccupied = bool_array
            SkillTreeBranchDef.Tiers[Tier].Skills = NewSkills
            SkillTreeBranchDef.Tiers[Tier].PointsToUnlockNextTier = min(MaxPoints, 5)
        # These are class specific skills that target the action skill of each class - Use each only with the corresponding class you use.
    ClassSkills = {
        "Soldier": [
            "GD_Soldier_Skills.Guerrilla.DoubleUp",
            "GD_Soldier_Skills.Guerrilla.LaserSight",
            "GD_Soldier_Skills.Guerrilla.ScorchedEarth",
            "GD_Soldier_Skills.Guerrilla.Sentry",
            "GD_Soldier_Skills.Gunpowder.Battlefront",
            "GD_Soldier_Skills.Gunpowder.LongBowTurret",
            "GD_Soldier_Skills.Gunpowder.Nuke",
            "GD_Soldier_Skills.Survival.Gemini",
            "GD_Soldier_Skills.Survival.Mag-Lock",
            "GD_Soldier_Skills.Survival.PhalanxShield",
        ],
        "Assassin": [
            "GD_Assassin_Skills.Bloodshed.Execute",
            "GD_Assassin_Skills.Bloodshed.Grim",
            "GD_Assassin_Skills.Bloodshed.ManyMustFall",
            "GD_Assassin_Skills.Cunning.DeathBlossom",
            "GD_Assassin_Skills.Cunning.Innervate",
            "GD_Assassin_Skills.Cunning.Unforseen",
        ],
        "Siren": [
            "GD_Siren_Skills.Cataclysm.ChainReaction",
            "GD_Siren_Skills.Cataclysm.Helios",
            "GD_Siren_Skills.Cataclysm.Ruin",
            "GD_Siren_Skills.Harmony.Elated",
            "GD_Siren_Skills.Harmony.Res",
            "GD_Siren_Skills.Harmony.SweetRelease",
            "GD_Siren_Skills.Harmony.Wreck",
            "GD_Siren_Skills.Motion.Converge",
            "GD_Siren_Skills.Motion.Quicken",
            "GD_Siren_Skills.Motion.SubSequence",
            "GD_Siren_Skills.Motion.Suspension",
            "GD_Siren_Skills.Motion.ThoughtLock",
        ],
        "Mercenary": [
            "GD_Mercenary_Skills.Brawn.AintGotTimeToBleed",
            "GD_Mercenary_Skills.Brawn.BusThatCantSlowDown",
            "GD_Mercenary_Skills.Brawn.ComeAtMeBro",
            "GD_Mercenary_Skills.Brawn.FistfulOfHurt",
            "GD_Mercenary_Skills.Gun_Lust.DivergentLikness",
            "GD_Mercenary_Skills.Gun_Lust.DownNotOut",
            "GD_Mercenary_Skills.Gun_Lust.KeepItPipingHot",
            "GD_Mercenary_Skills.Rampage.DoubleYourFun",
            "GD_Mercenary_Skills.Rampage.GetSome",
            "GD_Mercenary_Skills.Rampage.ImReadyAlready",
            "GD_Mercenary_Skills.Rampage.KeepFiring",
            "GD_Mercenary_Skills.Rampage.LastLonger",
            "GD_Mercenary_Skills.Rampage.SteadyAsSheGoes",
            "GD_Mercenary_Skills.Rampage.YippeeKiYay",
        ],
        "Lilac": [
            "GD_Lilac_Skills_Bloodlust.Skills.BloodTrance",
            "GD_Lilac_Skills_Bloodlust.Skills.BuzzAxeBombadier",
            "GD_Lilac_Skills_Bloodlust.Skills.TasteOfBlood",
            "GD_Lilac_Skills_Hellborn.Skills.HellfireHalitosis",
            "GD_Lilac_Skills_Mania.Skills.FuelTheRampage",
            "GD_Lilac_Skills_Mania.Skills.LightTheFuse",
            "GD_Lilac_Skills_Mania.Skills.ReleaseTheBeast",
        ],
        "Mechromancer": [
            "GD_Tulip_Mechromancer_Skills.BestFriendsForever.20PercentCooler",
            "GD_Tulip_Mechromancer_Skills.BestFriendsForever.BuckUp",
            "GD_Tulip_Mechromancer_Skills.BestFriendsForever.ExplosiveClap",
            "GD_Tulip_Mechromancer_Skills.BestFriendsForever.MadeOfSternerStuff",
            "GD_Tulip_Mechromancer_Skills.BestFriendsForever.PotentAsAPony",
            "GD_Tulip_Mechromancer_Skills.BestFriendsForever.SharingIsCaring",
            "GD_Tulip_Mechromancer_Skills.BestFriendsForever.UpshotRobot",
            "GD_Tulip_Mechromancer_Skills.EmbraceChaos.AnnoyedAndroid",
            "GD_Tulip_Mechromancer_Skills.EmbraceChaos.RobotRampage",
            "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.MakeItSparkle",
            "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.OneTwoBoom",
            "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.StrengthOfFiveGorillas",
            "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.TheStare",
        ],
    }
    # Any class should be able to use these.
    AnarchySkills = [
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.PreshrunkCyberpunk",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.Discord",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.TypecastIconoclast",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.RationalAnarchist",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.WithClaws",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.BloodSoakedShields",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.DeathFromAbove",
    ]

    BloodlustSkills = [
        "GD_Lilac_Skills_Bloodlust.Skills.BloodOverdrive",
        "GD_Lilac_Skills_Bloodlust.Skills.BloodyRevival",
        "GD_Lilac_Skills_Bloodlust.Skills.BloodBath",
        "GD_Lilac_Skills_Bloodlust.Skills.FuelTheBlood",
        "GD_Lilac_Skills_Bloodlust.Skills.BoilingBlood",
        "GD_Lilac_Skills_Bloodlust.Skills.NervousBlood",
        "GD_Lilac_Skills_Bloodlust.Skills.Bloodsplosion",
    ]
    # These skills are global, any class can use them!
    GlobalSkills = [
        "GD_Assassin_Skills.Bloodshed.Backstab",
        "GD_Assassin_Skills.Bloodshed.BeLikeWater",
        "GD_Assassin_Skills.Bloodshed.Followthrough",
        "GD_Assassin_Skills.Bloodshed.IronHand",
        "GD_Assassin_Skills.Bloodshed.KillingBlow",
        "GD_Assassin_Skills.Bloodshed.LikeTheWind",
        "GD_Assassin_Skills.Bloodshed.Resurgence",
        "GD_Assassin_Skills.Cunning.Ambush",
        "GD_Assassin_Skills.Cunning.CounterStrike",
        "GD_Assassin_Skills.Cunning.DeathMark",
        "GD_Assassin_Skills.Cunning.FastHands",
        "GD_Assassin_Skills.Cunning.Fearless",
        "GD_Assassin_Skills.Cunning.RisingShot",
        "GD_Assassin_Skills.Cunning.TwoFang",
        "GD_Assassin_Skills.Sniping.AtOneWithTheGun",
        "GD_Assassin_Skills.Sniping.Bore",
        "GD_Assassin_Skills.Sniping.CriticalAscention",
        "GD_Assassin_Skills.Sniping.HeadShot",
        "GD_Assassin_Skills.Sniping.KillConfirmed",
        "GD_Assassin_Skills.Sniping.Killer",
        "GD_Assassin_Skills.Sniping.OneShotOneKill",
        "GD_Assassin_Skills.Sniping.Optics",
        "GD_Assassin_Skills.Sniping.Precision",
        "GD_Assassin_Skills.Sniping.Velocity",
        "GD_Lilac_Skills_Bloodlust.Skills.BloodfilledGuns",
        "GD_Lilac_Skills_Bloodlust.Skills.BloodyTwitch",
        "GD_Lilac_Skills_Hellborn.Skills.BurnBabyBurn",
        "GD_Lilac_Skills_Hellborn.Skills.DelusionalDamage",
        "GD_Lilac_Skills_Hellborn.Skills.ElementalElation",
        "GD_Lilac_Skills_Hellborn.Skills.ElementalEmpathy",
        "GD_Lilac_Skills_Hellborn.Skills.FireFiend",
        "GD_Lilac_Skills_Hellborn.Skills.FlameFlare",
        "GD_Lilac_Skills_Hellborn.Skills.FuelTheFire",
        "GD_Lilac_Skills_Hellborn.Skills.NumbedNerves",
        "GD_Lilac_Skills_Hellborn.Skills.PainIsPower",
        "GD_Lilac_Skills_Hellborn.Skills.RavingRetribution",
        "GD_Lilac_Skills_Mania.Skills.EmbraceThePain",
        "GD_Lilac_Skills_Mania.Skills.EmptyRage",
        "GD_Lilac_Skills_Mania.Skills.FeedTheMeat",
        "GD_Lilac_Skills_Mania.Skills.PullThePin",
        "GD_Lilac_Skills_Mania.Skills.RedeemTheSoul",
        "GD_Lilac_Skills_Mania.Skills.SaltTheWound",
        "GD_Lilac_Skills_Mania.Skills.SilenceTheVoices",
        "GD_Lilac_Skills_Mania.Skills.StripTheFlesh",
        "GD_Lilac_Skills_Mania.Skills.ThrillOfTheKill",
        "GD_Mercenary_Skills.Brawn.Asbestos",
        "GD_Mercenary_Skills.Brawn.Diehard",
        "GD_Mercenary_Skills.Brawn.ImTheJuggernaut",
        "GD_Mercenary_Skills.Brawn.Incite",
        "GD_Mercenary_Skills.Brawn.JustGotReal",
        "GD_Mercenary_Skills.Brawn.OutOfBubblegum",
        "GD_Mercenary_Skills.Brawn.SexualTyrannosaurus",
        "GD_Mercenary_Skills.Gun_Lust.AllIneedIsOne",
        "GD_Mercenary_Skills.Gun_Lust.AutoLoader",
        "GD_Mercenary_Skills.Gun_Lust.ImYourHuckleberry",
        "GD_Mercenary_Skills.Gun_Lust.LayWaste",
        "GD_Mercenary_Skills.Gun_Lust.LockedandLoaded",
        "GD_Mercenary_Skills.Gun_Lust.MoneyShot",
        "GD_Mercenary_Skills.Gun_Lust.NoKillLikeOverkill",
        "GD_Mercenary_Skills.Gun_Lust.QuickDraw",
        "GD_Mercenary_Skills.Rampage.5Shotsor6",
        "GD_Mercenary_Skills.Rampage.AllInTheReflexes",
        "GD_Mercenary_Skills.Rampage.FilledtotheBrim",
        "GD_Mercenary_Skills.Rampage.Inconceivable",
        "GD_Siren_Skills.Cataclysm.Backdraft",
        "GD_Siren_Skills.Cataclysm.BlightPhoenix",
        "GD_Siren_Skills.Cataclysm.CloudKill",
        "GD_Siren_Skills.Cataclysm.Flicker",
        "GD_Siren_Skills.Cataclysm.Foresight",
        "GD_Siren_Skills.Cataclysm.Immolate",
        "GD_Siren_Skills.Cataclysm.Reaper",
        "GD_Siren_Skills.Harmony.LifeTap",
        "GD_Siren_Skills.Harmony.MindsEye",
        "GD_Siren_Skills.Harmony.Recompense",
        "GD_Siren_Skills.Harmony.Restoration",
        "GD_Siren_Skills.Harmony.Scorn",
        "GD_Siren_Skills.Harmony.Sustenance",
        "GD_Siren_Skills.Motion.Accelerate",
        "GD_Siren_Skills.Motion.Fleet",
        "GD_Siren_Skills.Motion.Inertia",
        "GD_Siren_Skills.Motion.KineticReflection",
        "GD_Siren_Skills.Motion.Ward",
        "GD_Soldier_Skills.Guerrilla.Able",
        "GD_Soldier_Skills.Guerrilla.CrisisManagement",
        "GD_Soldier_Skills.Guerrilla.Grenadier",
        "GD_Soldier_Skills.Guerrilla.Onslaught",
        "GD_Soldier_Skills.Guerrilla.Ready",
        "GD_Soldier_Skills.Guerrilla.Willing",
        "GD_Soldier_Skills.Gunpowder.DoOrDie",
        "GD_Soldier_Skills.Gunpowder.DutyCalls",
        "GD_Soldier_Skills.Gunpowder.Expertise",
        "GD_Soldier_Skills.Gunpowder.Impact",
        "GD_Soldier_Skills.Gunpowder.MetalStorm",
        "GD_Soldier_Skills.Gunpowder.Overload",
        "GD_Soldier_Skills.Gunpowder.Ranger",
        "GD_Soldier_Skills.Gunpowder.Steady",
        "GD_Soldier_Skills.Survival.Forbearance",
        "GD_Soldier_Skills.Survival.Grit",
        "GD_Soldier_Skills.Survival.HealthY",
        "GD_Soldier_Skills.Survival.LastDitchEffort",
        "GD_Soldier_Skills.Survival.Preparation",
        "GD_Soldier_Skills.Survival.Pressure",
        "GD_Soldier_Skills.Survival.QuickCharge",
        "GD_Tulip_Mechromancer_Skills.BestFriendsForever.CloseEnough",
        "GD_Tulip_Mechromancer_Skills.BestFriendsForever.CookingUpTrouble",
        "GD_Tulip_Mechromancer_Skills.BestFriendsForever.FancyMathematics",
        "GD_Tulip_Mechromancer_Skills.BestFriendsForever.TheBetterHalf",
        "GD_Tulip_Mechromancer_Skills.BestFriendsForever.UnstoppableForce",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.Anarchy",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.SmallerLighterFaster",
        "GD_Tulip_Mechromancer_Skills.EmbraceChaos.TheNthDegree",
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.ElectricalBurn",
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.EvilEnchantress",
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.InterspersedOutburst",
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.MorePep",
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.Myelin",
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.ShockAndAAAGGGHHH",
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.ShockStorm",
        "GD_Tulip_Mechromancer_Skills.LittleBigTrouble.WiresDontTalk",
    ]


Mod = CrossSkillModifier()
RegisterMod(Mod)