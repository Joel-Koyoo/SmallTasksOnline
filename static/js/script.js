
var btn = document.getElementById('menu-btn')
if (btn) {
   const nav = document.getElementById('menu')
   btn.addEventListener('click', () => {
      btn.classList.toggle('open');
      nav.classList.toggle('flex')
      nav.classList.toggle('hidden')
   })
}


function claimed_container() {
   const openBar = document.querySelector('#Open-Bar')
   const CloseBar = document.querySelector('#CloseBar')
   const SidebarParent = document.querySelector('.sidebar-parent')
   const Sidebar = document.getElementsByClassName('sidebar')[0]
   var removed = SidebarParent.removeChild(Sidebar);

   var claimed_container = document.getElementById("claimed-container")


   CloseBar.addEventListener('click', () => {

      claimed_container.className = "ml-20 text-left bg-white"
   })

   openBar.addEventListener('click', () => {


      SidebarParent.appendChild(removed)
      claimed_container.className = "md:ml-[330px] text-left bg-white"



   })


}
function CloseTask() {
   var openBar = document.querySelector('#Open-Bar')
   var CloseBar = document.querySelector('#CloseBar')
   var SidebarParent = document.querySelector('.sidebar-parent')
   var Sidebar = document.getElementsByClassName('sidebar')[0]
   var removed = SidebarParent.removeChild(Sidebar);

   var deadline = document.getElementById("deadline")
   var taskpool_container = document.getElementById("taskpool-container")
   var proposed_price = document.getElementById("proposed-price")


   CloseBar.addEventListener('click', () => {

      deadline.className = "hidden md:table-cell md:table-cell whitespace-nowrap  text-center p-3 text-base text-gray-700"

      taskpool_container.className = "w-full mx-auto text-center bg-white"

      proposed_price.className = "hidden whitespace-nowrap md:table-cell md:p-3 text-base text-center font-semibold tracking-wide text-center"



   })

   openBar.addEventListener('click', () => {

      SidebarParent.appendChild(removed)

      deadline.className = "hidden md:table-cell md:table-cell md:w-20 text-center p-3 text-base text-gray-700"

      taskpool_container.className = "md:ml-[200px] text-center bg-white"

      proposed_price.className = "hidden md:table-cell md:p-3 text-base text-center font-semibold tracking-wide text-center"




   })


}

function Close() {
   const openBar = document.querySelector('#Open-Bar')
   const CloseBar = document.querySelector('#CloseBar')
   const SidebarParent = document.querySelector('.sidebar-parent')
   const Sidebar = document.getElementsByClassName('sidebar')[0]
   var removed = SidebarParent.removeChild(Sidebar);

   var cardbox = document.getElementById("cardbox")
   var table = document.getElementById("table")
   var dashboard_container = document.getElementById("dashboard-container")

   var deadline = document.getElementById("deadline")



   var tabledata = document.getElementsByTagName("td")




   CloseBar.addEventListener('click', () => {

      // SidebarParent.removeChild(Sidebar);
      dashboard_container.className = "w-5/6 mx-auto text-center bg-white"



      cardbox.className = "py-4 text-center items-center bg-white";


      table.className = "w-full text-center items-center bg-white";

      tabledata.className = "hidden md:table-cell md:table-cell md:w-full whitespace-nowrap text-left p-3 text-base text-gray-700"

      deadline.className = "hidden md:table-cell md:table-cell whitespace-nowrap  text-center p-3 text-base text-gray-700"



   })

   openBar.addEventListener('click', () => {

      SidebarParent.appendChild(removed)

      dashboard_container.className = "md:ml-[200px] text-center bg-white"

      cardbox.className = "py-4 md:ml-[300px] text-center sm:items-center bg-white";

      table.className = "w-5/6 mx-auto md:ml-[150px]";


   })

}



function Report_container() {
   const openBar = document.querySelector('#Open-Bar')
   const CloseBar = document.querySelector('#CloseBar')
   const SidebarParent = document.querySelector('.sidebar-parent')
   const Sidebar = document.getElementsByClassName('sidebar')[0]
   var removed = SidebarParent.removeChild(Sidebar);

   var Report_container = document.getElementById('Report-container')


   CloseBar.addEventListener('click', () => {

      // SidebarParent.removeChild(Sidebar);
      Report_container.className = "text-left bg-white"


   })

   openBar.addEventListener('click', () => {

      SidebarParent.appendChild(removed)

      Report_container.className = "md:ml-[200px] text-left bg-white"

   })

}


function ContactClose() {
   const openBar = document.querySelector('#Open-Bar')
   const CloseBar = document.querySelector('#CloseBar')
   const SidebarParent = document.querySelector('.sidebar-parent')
   const Sidebar = document.getElementsByClassName('sidebar')[0]
   var removed = SidebarParent.removeChild(Sidebar);

   var contact = document.getElementById('contactUs')


   CloseBar.addEventListener('click', () => {

      // SidebarParent.removeChild(Sidebar);
      contact.className = ""


   })

   openBar.addEventListener('click', () => {

      SidebarParent.appendChild(removed)

      contact.className = "md:ml-[300px]"

   })

}

function submitted() {
   const openBar = document.querySelector('#Open-Bar')
   const CloseBar = document.querySelector('#CloseBar')
   const SidebarParent = document.querySelector('.sidebar-parent')
   const Sidebar = document.getElementsByClassName('sidebar')[0]
   var removed = SidebarParent.removeChild(Sidebar);

   var submitted_container = document.getElementById('submitted-container')


   CloseBar.addEventListener('click', () => {

      // SidebarParent.removeChild(Sidebar);
      submitted_container.className = "mx-auto text-left bg-white"


   })
   
   openBar.addEventListener('click', () => {

      SidebarParent.appendChild(removed)

      submitted_container.className = "md:ml-[330px] text-left bg-white"

   })




   console.log(submitted_container.className)

}
function TaskClose() {
   const openBar = document.querySelector('#Open-Bar')
   const CloseBar = document.querySelector('#CloseBar')
   const SidebarParent = document.querySelector('.sidebar-parent')
   const Sidebar = document.getElementsByClassName('sidebar')[0]
   var removed = SidebarParent.removeChild(Sidebar);

   var taskbar = document.getElementById('taskbar')


   CloseBar.addEventListener('click', () => {

      // SidebarParent.removeChild(Sidebar);
      taskbar.className = "mt-12"


   })

   openBar.addEventListener('click', () => {

      SidebarParent.appendChild(removed)

      taskbar.className = "md:ml-[280px] mt-12"

   })

}

function Profile() {
   const openBar = document.querySelector('#Open-Bar')
   const CloseBar = document.querySelector('#CloseBar')
   const SidebarParent = document.querySelector('.sidebar-parent')
   const Sidebar = document.getElementsByClassName('sidebar')[0]
   var removed = SidebarParent.removeChild(Sidebar);

   var Profile = document.getElementById('Profile')


   CloseBar.addEventListener('click', () => {

      // SidebarParent.removeChild(Sidebar);
      Profile.className = "w-5/6 mx-2 my-2 md:w-1/2 mt-12 mx-auto mx-auto md:ml-[310px]"


   })

   openBar.addEventListener('click', () => {

      SidebarParent.appendChild(removed)

      Profile.className = "w-5/6 mx-2 my-2 md:w-1/2 mt-12 mx-auto md:ml-[310px]"

   })

}



if (document.URL.includes("/taskpool/")) {
   function alljoined() {
      CloseTask();
   }


}

else if (document.URL.includes("/dashboard/")) {
   function alljoined() {
      Close();
   }
}

else if (document.URL.includes("SubmittedTasks/")) {
   function alljoined() {
      submitted()
   }
}

else if (document.URL.includes("ClaimedTasks/")) {
   function alljoined() {
      claimed_container()
   }
}

else if (document.URL.includes("create_Task/")) {
   function alljoined() {
      TaskClose()
   }
}
else if (document.URL.includes("ContactUs/")) {
   function alljoined() {
      ContactClose()
   }

}

else if (document.URL.includes("ReportPoolPage/")) {
   function alljoined() {
      Report_container()
   }

}
else {
   function alljoined() {
      Profile()
   }
}

