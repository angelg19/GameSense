# services/rivals_context.py

#Additional context for Marvel Rivals to be used by the LLMs.

rivals_context = {
    "Practice regiments":  
            """PRACTICE REGIMENTS:
            Strategists: Practicing with a strategist is a bit different from practicing with other heroes. Typically the practice range
            is not as useful for strategists since getting kills or hitting combos is not your main focus. 
            Thus it is better to practice strategists by playing actual games, usually quick matches, depending on your familiarity 
            with the hero. Awareness and game sense are key for playing a strategist well, as there are many things you need to keep track of.
            Such as the health of you and your enemies, prioritize healing the players closest to death, even if that means yourself.
            You also need to keep track of the enemies and their positioning, if you get dove there are heroes that can kill you within seconds,
            so you need to call for help when you sense enemies approaching you.
            You want to keep your death count low as possible as a strategist, because the rest of the team staying alive relies on you
            being able to heal them. When you do die in game, go back and analyze what caused your death there so you can try and avoid 
            making the same mistakes in future games. Knowing when to pop your strategist ultimate is crucial to every game. 
            
            Vanguards: 

            Duelists: With duelists being the majority of the heroes, it's hard to create one single training routine that applies to them all.
            For hit-scan, poke, or aim reliant heroes, the practice range is the best
            Effectiveness with dive heroes is all about how much damage you can put out in the least amount of time possible.
            To do this well you will need to get all your combos down and know exactly how to chain attacks together even when you miss one.""",
    
    "Team compositions":   
            """TEAM COMPOSITIONS:
            A team composition (comp) consists of three numbers that must add up to the 6 players on one team, the numbers, in order,
            refer to the number of vanguards, then duelists, then strategists respectively. 
            For example, a 2-1-3 composition refers to a team with 2 vanguards, 1 duelist, and 3 strategists.
            Any team composition not listed below that make up 6 members you are technically allowed to play, 
            but is not recommended due to a very poor balance:
                1-3-2: This composition is not recommended for any rank higher than diamond.
                2-2-2: This composition is very common and provides a good balance
                3-1-2: Not typically recommended, this puts a high strain on your healers since they have to heal 3 tanks.
                1-2-3: Has potential value depending on the other teams composition, you may want to play this when you
                need a high damage output, as duelists typically are better at this than vanguards. However it is typically better
                to play a 2-1-3 composition if you want 3 healers. Your vanguard holds the team together in this comp.
                2-1-3: One of the best compositions in the game, allows your third healer to act as both a healer and duelist,
                switching between getting kills and keeping the team alive depending on the situation.
                3-0-3: Popular in top ranks (Eternity+) and gets seen a lot in pro level tournaments. With this composition
                you'll want to make sure your vanguards are also going for kills on strategists rather than staying in the front lines.""",

    "Terms": """TERMS:
            Backline: Refers to strategists and heroes that play furthest from the main battle.
            Squishies: Refers to characters with the lowest base health in the game (250 hp), typically strategists.
            Peel: Refers to teammates retreating to the backlines to help strategists survive, often because they are being
                pressured by dive characters.
            Patty-caking/pattycake: A technique used by two healers where they solely focus on healing only each other. This can keep both 
                strategists alive in situations where they would usually end up dead by keeping focusing their high healing outputs
                on one target each.
            Tank = Vanguard
            Healer = Strategist = Support
            Lord / Lord Icon: Refers to the icon you get after playing a hero for usually about 25-30 hours. This icon is seen by other players
                as well when you select that hero in-match, meaning others will know if you are familiar with that hero.
                Usually having a lord icon implies you are skilled with them, but this isn't always the case.
            Off-tank: A vanguard that doesn't play the tank role how you normally should by eating the hits for your team.
                Instead you might not be in the front line at all times. Examples include Venom, Captain America, and Hulk (These vanguards
                all typically attack the enemy backline).
            Solo-tanking: When your team has only one vanguard.
            Poke heros: Typically referring to duelists, heroes that fire projectiles and do damage from range with their primary fire.
            Dive heroes: Typically referring to duelists, heroes that target the enemy backline with fast combos and movement. 
              Their strategy is typically:
                1. Hide until you see an enemy/enemies who is/are vulnerable.
                2. Dive and eliminate them as fast as you can while taking as little damage as possible.
                3. Take cover and get your health back to full.
                4. Repeat cycle.
            C9: Your team leaves the objective at a crucial time and gets punished for it. This often results in the enemy reaching a checkpoint
            or your team losing if you were on offense.""",

        "Gen_Prompt": """
            CONTEXT: 
            General rules of Competitive play: 
            1. Ranks - This is a list of all ranks in order in Marvel Rivals (Note that every rank except for 'One Above All' and 'Eternity' have 
            three subdivisions ascending from 3 to 2 to 1): ['Bronze','Silver','Gold','Platinum','Diamond','Grandmaster', 'Celestial', 'Eternity', 'One Above All']
            Players ranked Gold or lower can queue with each other at all times. Players ranked higher can only queue with players who
            are within one rank of them, for instance Diamond 2 players can play with Grandmaster 2 players but not Grandmaster 1 
            (Eternity to One Above All counts as one rank). 
            For players ranked Eternity or higher, only duo and solo queuing are allowed.
            2. Bans - When all members of a match are ranked Gold or higher, each team will be allowed to ban 2 heroes which neither team will be able to play.
            Two separate ban selections are done for each team simultaneously through a team vote, which will be decided by random selection of all votes.
            One hero can be banned twice if both teams choose them in the same selection. Also if nobody on a team votes, that team will skip a ban (ban nobody).
            Ban votes can be seen by all team members, and multiple votes for the same hero results in a higher chance of being selected.
            3. Hero swaps - Players can swap heroes an unlimited amount of times if they are within the confines of their own team spawn and select
            a hero not currently chosen by another teammate. There is
            a limit of 1 unique hero per team, meaning two players cannot play the same hero. If you do swap and your 
            ultimate ability charge was higher than 50% it will be cut down to 50%, all other abilities cooldowns are reset.
            4. Ability cooldowns - Ability and Ultimate status do not persist across multiple rounds for Convoy and Convergence, however they 
            do persist for Domination. Ability cooldowns are on a per team basis, meaning the entire team shares one cooldown for each hero.
            Cooldowns last through deaths too, however this mainly matters for a few extra long cooldowns that exist within the game.
            However this does not apply for ultimate status, ultimate charges are on a per player basis.
            5. Spawns - Rivals competitive modes are all unlimited respawns, meaning you have an infinite number of lives at all times.
            After a death, it takes about 12 seconds to respawn back in your teams respawn zone, this time never changes. You are safe from enemy damage
            within this spawn, which is a room marked by green doorways as their exits, once leaving these doorways you are vulnerable.
            6. Health packs - There are multiple health packs located across every map, these health packs grant
            around 200-250 health and have a reset time of about 15 seconds after being used. Any player can use them by running over it.
            Only one player can use at a time no matter what.
            7. Friendly fire - There is no friendly fire of any kind within Marvel Rivals. Players can only be healed by their teammates, and a few niche moves
            can alter the movement speed or movement type of allies.
            8. Getting Kills, Assists: A kill is rewarded to players if they damaged the enemy and that enemy is then eliminated by them or another
            teammate. An assist is provided only if you healed your teammate or provided some special effect on them and they get an elimination.
            An assist will only be provided if the effect you provided is still active, or if only a short duration of time has passed since you healed them.
            Assist stats may look very low for some heroes, this does not necessarily mean they aren't being played well, just that some heroes
            are very hard to get assists with if they dont have some sort of healing or team effect.

            Starting with the objective of the game, within competitive play there are three separate modes, Convoy, Convergence, and Domination.
            All modes are played 6v6:
            1. Convoy: Capture the objective (a moving cart) and push it towards the end goal before your initial timer of 4 minutes
            runs out, once the timer runs out the teams on offense and defense will switch. The team who moves it further on
            the map will be the winner, measured by how many meters from the cart's starting position you have pushed it. 
            If both teams reach the end goal or neither team moves a single meter from the starting position,
            there will be 2 overtime rounds with a shorter clock. If there is a tie in overtime the game will end in a draw.
            There are two checkpoints that will grant a time boost if reached, in overtime rounds if a checkpoint is reached no 
            additional time is granted. Reaching checkpoints will also change the respawn point for each team,
            with both moving closer to the end goal. Typically the team on offense has their respawn set up 
            close to the newly captured checkpoint, and the defending team will be moved near the next checkpoint.
            The cart can still move after the clock hits zero but there needs to be
            a member from the team on offense contesting the cart at all times. Team members may only leave the cart for a
            total of 3 seconds in this "mini overtime", but any time beyond that will result in the round ending. Leaving and recontesting
            the cart does not reset this 3 second timer. As soon as the second team going second passes the distance that the first team
            pushed the cart to, the game will end with the second team winning.
            Cart mechanics - at any given moment the cart can either move forward, backward, or stay still. 
            The cart stays still when at least one member from each team are contesting it simultaneously. The cart has 4 different speeds when
            moving forward, the fastest being 3 members on offense contesting the cart, and the slowest being 0 members contesting.
            The cart only has one speed moving backward. The cart can move even once the timer hits 0 if a player on offense is contesting.
            In order to capture the cart you must be in a radius of 3-4 meters from the cart.
            
            2. Convergence: This mode is exactly the same as Convoy, except that the first checkpoint involves capturing a zone rather than 
            moving the cart to a certain spot. Once you capture this zone, the cart will spawn in and there will only be one more checkpoint 
            you must reach before the end goal. This initial zone counts as a checkpoint, thus you will have a new
            respawn point once you fully capture it. This initial zone takes about 10 seconds to capture and can be sped up
            with multiple members contesting at once. You cannot increase capture progress on the zone while the defending
            team is contesting. If the enemy team contests while you have progress on the zone they will reverse your progress.
            If one or more members from each team is contesting neither side will be able to make progress on the zone. 
            There are 3 subsections to capturing this point, for each third of the objective
            you capture you will no longer be able to go under that, even if the other team captures the zone and decreases your percentage.
            After capturing the zone, the cart will take about 10 seconds to spawn in and start moving.
            
            3. Domination: A best of 3 fast paced game mode, played on 3 separate maps. Capture the single objective zone in the center 
            of the map and reach 100% capture completion before the opposing team. The objective starts in a neutral setting until one team captures it.
            To capture the objective you must contest it while there are no opposing team members contesting for about 4-5 sec, 
            the zone typically spans about 8 meters x 8 meters x 10 meters (vertical for fliers to contest). In Domination, neither teams respawn point will
            change under any circumstances, unless it is a map change across rounds. The speed at which you capture the objective increases with the more players
            you have contesting the point, but once captured, your capture percentage will increase at a constant rate until the other team fully captures the objective.
            Very important note, if one or more members from each team are contesting the objective at the same time, neither team can make
            capture progress, however you will continue gaining completion percentage if you previously had captured the objective.
            In other words, the only way to stop your opponents completion 
            percentage from rising, is to fully capture the objective yourself. At the moment either team hits 99% completion percentage, the opposing team 
            must be contesting the objective or the round will end. If the opposing team is contesting when the completion percentage hits 99%,
            the game will go into overtime, this overtime CAN ONLY END once there only remains members from a single team contesting the objective.
            In overtime, if the team that reached 99% stops contesting and the other team keeps contesting, then they will
            capture the objective and the game will continue like before where their completion percentage will rise.
            Overtime will last as long as it needs to, with no time limits, there are no ties in Domination.

            META:
            These are a few abilities you must always be aware of that are crucial to many games.
            Doctor Strange portal: over 2 minute cooldown, allows you to place a portal between any two locations on the map.
            Very useful for getting a last second contest when your spawn is far away from the objective and time is running out or your
            opponent is about the capture a checkpoint/win the game. You should try to use this every game.
            If doctor strange is hit with a stun ability while he is casting the opening and exit portals, his cooldown will be activated but no portal will be placed.
            This counter is often done by spiderman as he can move quickly around the map with web swings. Your team
            should protect you while casting your portal. Since Doctor Strange is a vanguard, make sure one of your non strategist teammates
            switches to him if making a last second hero switch so you can keep at least two healers on your team for the fight.

            Magneto Bubble: Magneto places a bubble around himself or teammates making them invulnerable from one shot moves/combos. This
            is very useful in situations where your teammates are vulnerable or have predictable movement. Used very commonly on strategists
            when they are popping their ultimate, cloak and dagger especially has predictable movement. This ability has a short cooldown
            of 8 seconds so make sure you don't pop it right before your teammate may need it.

            Jeff The Land Shark ultimate: Jeff can swallow players on the map within his ability radius and keep them in his stomach for
            about 7-8 seconds. Note that both your teammates and opponents can be swallowed, which can help or hurt you when
            you want to swallow anybody contesting the objective. Often used as a suicide method by jumping off the map to kill
            all the enemies you swallowed. Make sure that you wait the full 8 seconds before spitting enemies out / jumping off the map.
            The 100 meter jeff ultimate is a technique where you activate your ultimate far away to avoid enemies hearing the audio queue, and
            then you have an 8 second window to move over to the battle before actually swallowing which is about 100 meters. Works well in triple
            support comps.

            Adam Warlock ultimate: Adam can resurrect all teammates within a certain radius of him after casting his ultimate. You must die within
            this radius to be respawned at the location Adam used his ultimate in. Similar to a Doctor Strange portal, this ability can give
            a team another chance when the clock is running down or even at 0 and overtime has begun. This ability is even better than a Strange portal
            because it eliminates the 12 seconds it normally takes to respawn and instantly takes you back to the fight. This ultimate must be placed
            in a strategic spot or else your team can be wiped again easily as soon as they spawn in. Works well in triple support comps.

            Damage Boosts: Can help kill heroes through bonus shields and strategist ultimates.
            There are multiple heroes that can provide damage boosts to themselves and their teammates, mainly: mantis, rocket raccoon.

            Gambit cleanse: Gambit can remove all enemy effects on teammates within his ability radius. Only Hulk's exile effect cannot be removed.
            Useful for removing stuns / slows, anti-heal effects, or ability effects such as Winter Soldier's ultimate. Best used for countering vanguard ultimates.

                
            GENERAL TIPS TO REMEMBER:
            1. Strategist Ultimates are the key to almost every single game. Knowing when to use them and when not to use them is
            crucial for becoming a great player. DO NOT DOUBLE STRATEGIST ULTIMATES. This means do not use two of them at a time, the only 
            exception to this is for non typical strategist ultimates such as Jeff or Ultron's whose primary function isn't necessarily healing.
            2. Use natural cover as much as possible. This is a very important tip that is seen in all high level play and pro tournaments. 
            It's often overlooked in lower ranks but it is a crucial technique in Rivals and can help to minimize the damage you take 
            and avoid unnecessary deaths.
            3. Pattycake with other healers to counter duelist ultimates. This is a technique used by two healers where they solely focus 
            on healing only each other. This can keep both strategists alive in situations where they would usually end up dead by keeping 
            focusing their high healing outputs on one target each.
            4. Do not stagger. If you are outnumbered heavily in a fight, it is always better to retreat and wait for your team to respawn
            rather than trying to fight a losing battle. The only exception to this is when you need to contest an objective at all costs.
            Such as the final seconds of a Domination round or when the cart is about to reach a checkpoint. In those cases you should attempt
            to stall the objective as long as you can to buy enough time for your teammates to return.

        """

}


map_context =  {

    1230: {'game_mode': 'Convergence', 'name': 'Shin-Shibuya', 'location': 'Tokyo 2099'},
    1231: {'game_mode': 'Convoy', 'name': 'Yggdrasill Path', 'location': 'Yggsgard'},
    1236: {'game_mode': 'Domination', 'name': 'Royal Palace', 'location': 'Yggsgard'},
    1245: {'game_mode': 'Convoy', 'name': 'Spider-Islands', 'location': 'Tokyo 2099'},
    1267: {'game_mode': 'Convergence', 'name': 'Hall of Djalia', 'location': 'Intergalactic Empire of Wakanda'},
    1272: {'game_mode': 'Domination', 'name': "Birnin T'Challa", 'location': 'Intergalactic Empire of Wakanda'},
    1288: {'game_mode': 'Domination', 'name': "Hell's Heaven", 'location': 'Hydra Charteris Base'},
    1290: {'game_mode': 'Convergence', 'name': 'Symbiotic Surface', 'location': 'Klyntar'},
    1291: {'game_mode': 'Convoy', 'name': 'Midtown', 'location': 'Empire of Eternal Night'},
    1292: {'game_mode': 'Convergence', 'name': 'Central Park', 'location': 'Empire of Eternal Night'},
    1310: {'game_mode': 'Domination', 'name': 'Krakoa', 'location': 'Hellfire Gala'},
    1311: {'game_mode': 'Convoy', 'name': 'Arakko', 'location': 'Hellfire Gala'},
    1318: {'game_mode': 'Domination', 'name': 'Celestial Husk', 'location': 'Klyntar'},
    1320: {'game_mode': 'RESOURCE RUMBLE', 'name': 'THRONE OF KNULL', 'location': ''},
    2042: {'game_mode': 'CONVERGENCE', 'name': 'HEART OF HEAVEN', 'location': "Ku'n-Lun"},

}