class CompaniesController < InheritedResources::Base


def new
  @company = Company.new
end

def create
  @company = Company.new(company_params)
  @company.user_id = current_user.id

  if @company.save
    redirect_to root_path
  else
    render 'new'
  end
  
end



  private

    def company_params
      params.require(:company).permit(:name, :user_id)
    end
end

